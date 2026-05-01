from pathlib import Path
from typing import List

from engine.context.models import ContextDocument


def load_local_markdown_documents(path: str) -> List[ContextDocument]:
    docs_path = Path(path)

    if not docs_path.exists():
        raise FileNotFoundError(f"Documentation file not found: {docs_path}")

    content = docs_path.read_text(encoding="utf-8")

    sections = []
    current_title = None
    current_lines = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_title and current_lines:
                sections.append(
                    ContextDocument(
                        id=current_title.lower().replace(" ", "_"),
                        title=current_title,
                        content="\n".join(current_lines).strip(),
                        source=str(docs_path),
                    )
                )

            current_title = line.replace("## ", "").strip()
            current_lines = []
        else:
            if current_title:
                current_lines.append(line)

    if current_title and current_lines:
        sections.append(
            ContextDocument(
                id=current_title.lower().replace(" ", "_"),
                title=current_title,
                content="\n".join(current_lines).strip(),
                source=str(docs_path),
            )
        )

    return sections