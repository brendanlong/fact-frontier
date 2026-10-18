import os
import sqlite3
import time
from dataclasses import dataclass
from typing import Literal

import numpy as np
from openai import OpenAI
from pydantic import BaseModel

Effort = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class Models:
    extract: str = "anthropic/claude-sonnet-5.5"
    merge: str = "anthropic/claude-sonnet-5.5"
    name_clusters: str = "anthropic/claude-haiku-5.5"
    embed: str = "voyageai/voyage-4"


class LLMError(RuntimeError):
    pass


class LLM:
    def __init__(self, conn: sqlite3.Connection, models: Models | None = None):
        self.conn = conn
        # Held until flush_log() so that a step which fails and rolls back still records what
        # it spent: callers flush after their commit or rollback.
        self.pending: list[tuple] = []
        self.models = models or Models()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            default_headers={"X-OpenRouter-Title": "fact-frontier"},
            timeout=600,
        )

    def structured[T: BaseModel](
        self,
        purpose: str,
        model: str,
        schema: type[T],
        system: str,
        user: str,
        effort: Effort = "medium",
    ) -> T:
        start = time.monotonic()
        resp = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "strict": True,
                    "schema": strict_schema(schema),
                },
            },
            max_tokens=64000,
            extra_body={"reasoning": {"effort": effort}},
        )
        self._log(purpose, model, resp.usage, time.monotonic() - start)
        # OpenRouter reports an upstream failure after the response opened as a 200 with an
        # `error` field and no usable choice.
        error = getattr(resp, "error", None)
        if error or not resp.choices:
            raise LLMError(f"{purpose}: {error or 'no choices'}")
        choice = resp.choices[0]
        if choice.finish_reason == "length":
            raise LLMError(f"{purpose}: output hit max_tokens")
        return schema.model_validate_json(choice.message.content or "")

    def embed(self, texts: list[str]) -> np.ndarray:
        """Unit-normalized embeddings, one row per text."""
        start = time.monotonic()
        rows: list[list[float]] = []
        for i in range(0, len(texts), 128):
            resp = self.client.embeddings.create(model=self.models.embed, input=texts[i : i + 128])
            rows.extend(d.embedding for d in sorted(resp.data, key=lambda d: d.index))
            self._log("embed", self.models.embed, resp.usage, time.monotonic() - start)
            start = time.monotonic()
        vecs = np.array(rows, dtype=np.float32)
        return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)

    def _log(self, purpose: str, model: str, usage, seconds: float) -> None:
        extra = (usage.model_extra or {}) if usage else {}
        details = getattr(usage, "prompt_tokens_details", None)
        self.pending.append(
            (
                purpose,
                model,
                getattr(usage, "prompt_tokens", 0) or 0,
                getattr(usage, "completion_tokens", 0) or 0,
                getattr(details, "cached_tokens", 0) or 0,
                extra.get("cost", 0.0),
                seconds,
            )
        )

    def flush_log(self) -> None:
        self.conn.executemany(
            "INSERT INTO llm_calls (purpose, model, prompt_tokens, completion_tokens,"
            " cached_tokens, cost, seconds) VALUES (?, ?, ?, ?, ?, ?, ?)",
            self.pending,
        )
        self.conn.commit()
        self.pending.clear()

    def pending_cost(self) -> float:
        return sum(row[5] for row in self.pending)


def strict_schema(model: type[BaseModel]) -> dict:
    """Pydantic's JSON schema, tightened to what strict structured outputs require: every
    property required and no additional properties, on every object including nested ones."""
    schema = model.model_json_schema()

    def tighten(node: dict) -> None:
        node.pop("title", None)
        node.pop("default", None)
        if "properties" in node:
            node["required"] = list(node["properties"])
            node["additionalProperties"] = False
            for prop in node["properties"].values():
                tighten(prop)
        for key in ("items", "anyOf", "allOf", "$defs"):
            child = node.get(key)
            if isinstance(child, dict):
                for sub in child.values() if key == "$defs" else [child]:
                    tighten(sub)
            elif isinstance(child, list):
                for sub in child:
                    tighten(sub)

    tighten(schema)
    return schema
