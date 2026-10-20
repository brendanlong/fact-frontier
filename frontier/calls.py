"""Model calls that leave a complete, inspectable record.

Every call writes its full input and output to an artifact file and an `artifacts` row on a
connection of its own that commits immediately, so the record survives whatever happens to the
caller's transaction. Callers should make their model calls before opening a write transaction
on the main connection.
"""

import hashlib
import json
import os
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

from frontier import store
from frontier.llm import strict_schema

Effort = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Roles:
    """Pinned model per role. Changing one means re-running the acceptance set."""

    map: str = "anthropic/claude-opus-5.5"
    guide: str = "anthropic/claude-opus-5.5"
    gold_draft: str = "openai/gpt-6.1-sol"
    exam: str = "openai/gpt-6.1-sol"
    # Different family from the guide it judges, to avoid self-preference.
    matcher: str = "openai/gpt-6.1-sol"
    canary: str = "anthropic/claude-opus-5.5"
    self_test: str = "anthropic/claude-sonnet-5.5"
    # A different family from the writer, reading each question with no other context.
    standalone_judge: str = "openai/gpt-6.1-sol"
    embed: str = "voyageai/voyage-4"


class CallFailed(RuntimeError):
    def __init__(self, artifact_id: str, message: str):
        super().__init__(f"{message} (artifact {artifact_id})")
        self.artifact_id = artifact_id


class Client:
    def __init__(self, db_path: Path, artifacts_dir: Path, roles: Roles | None = None):
        self.log = store.connect(db_path)
        self.log.isolation_level = None
        self.artifacts_dir = artifacts_dir
        self.roles = roles or Roles()
        self.api = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            default_headers={"X-OpenRouter-Title": "fact-frontier"},
            timeout=1800,
            max_retries=2,
        )

    def structured[T: BaseModel](
        self,
        stage: str,
        model: str,
        schema: type[T],
        system: str,
        user: str,
        *,
        subject: str | None = None,
        effort: Effort = "medium",
        max_tokens: int = 64000,
        validate: Callable[[T], None] | None = None,
    ) -> tuple[T, str]:
        """Returns the parsed result and its artifact ID. Raises CallFailed (after recording
        the artifact) on API errors, truncation, output that doesn't match the schema, or output
        that `validate` rejects (recorded as `rejected`)."""
        artifact_id = f"{stage}-{uuid.uuid4().hex[:12]}"
        json_schema = strict_schema(schema)
        params = {
            "effort": effort,
            "max_tokens": max_tokens,
            "input_sha": hashlib.sha256(user.encode()).hexdigest()[:16],
        }
        prompt_hash = hashlib.sha256(
            json.dumps([system, json_schema], sort_keys=True).encode()
        ).hexdigest()[:16]
        record: dict = {
            "artifact_id": artifact_id,
            "stage": stage,
            "subject": subject,
            "model": model,
            "params": params,
            "schema_name": schema.__name__,
            "system": system,
            "user": user,
        }
        start = time.monotonic()
        resp = None
        try:
            resp = self.api.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {"name": schema.__name__, "strict": True, "schema": json_schema},
                },
                max_tokens=max_tokens,
                extra_body={"reasoning": {"effort": effort}},
            )
            record["response"] = resp.model_dump()
            error = getattr(resp, "error", None)
            if error or not resp.choices:
                raise ValueError(f"upstream error: {error or 'no choices'}")
            choice = resp.choices[0]
            if choice.finish_reason == "length":
                raise ValueError("output hit max_tokens")
            parsed = schema.model_validate_json(choice.message.content or "")
        except BaseException as e:
            self._save(record, resp, "failed", repr(e), time.monotonic() - start, prompt_hash)
            raise CallFailed(artifact_id, f"{stage} call failed: {e}") from e
        if validate:
            try:
                validate(parsed)
            except ValueError as e:
                self._save(record, resp, "rejected", repr(e), time.monotonic() - start, prompt_hash)
                raise CallFailed(artifact_id, f"{stage} output rejected: {e}") from e
        self._save(record, resp, "ok", None, time.monotonic() - start, prompt_hash)
        return parsed, artifact_id

    def embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for i in range(0, len(texts), 128):
            resp = self.api.embeddings.create(model=self.roles.embed, input=texts[i : i + 128])
            out.extend(d.embedding for d in sorted(resp.data, key=lambda d: d.index))
        return out

    def _save(self, record, resp, outcome, error, seconds, prompt_hash) -> None:
        path = self.artifacts_dir / record["stage"] / f"{record['artifact_id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=1, default=str))
        usage = getattr(resp, "usage", None)
        extra = (usage.model_extra or {}) if usage else {}
        self.log.execute(
            "INSERT INTO artifacts (artifact_id, stage, subject, requested_model, served_model,"
            " provider, prompt_hash, schema_name, params, path, outcome, error, prompt_tokens,"
            " completion_tokens, cost, seconds) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                record["artifact_id"],
                record["stage"],
                record["subject"],
                record["model"],
                getattr(resp, "model", None),
                getattr(resp, "provider", None),
                prompt_hash,
                record["schema_name"],
                json.dumps(record["params"]),
                str(path),
                outcome,
                error,
                getattr(usage, "prompt_tokens", None),
                getattr(usage, "completion_tokens", None),
                extra.get("cost"),
                seconds,
            ),
        )
