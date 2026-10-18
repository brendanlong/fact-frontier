import re
import subprocess
import urllib.request
from pathlib import Path

ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def resolve(arg: str, cache_dir: Path) -> tuple[str, Path]:
    """Map a CLI argument (arXiv ID, arXiv URL, or local PDF path) to a stable ref and a local
    PDF. Local files named like arXiv downloads get the arXiv ref, so the same paper ingested
    either way is recognized as one source."""
    path = Path(arg)
    if path.exists():
        m = ARXIV_ID.search(path.name)
        return (f"arxiv:{m.group(1)}" if m else f"file:{path.name}"), path
    m = ARXIV_ID.search(arg)
    if not m:
        raise ValueError(f"not a file or arXiv ID: {arg}")
    arxiv_id = m.group(1) + (m.group(2) or "")
    pdf = cache_dir / f"{arxiv_id}.pdf"
    if not pdf.exists():
        cache_dir.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(f"https://arxiv.org/pdf/{arxiv_id}", pdf)
    return f"arxiv:{m.group(1)}", pdf


def pdf_text(pdf: Path) -> str:
    out = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True)
    # Form feeds mark page breaks; runs of blank lines are layout noise.
    return re.sub(r"\n{3,}", "\n\n", out.stdout.replace("\f", "\n"))
