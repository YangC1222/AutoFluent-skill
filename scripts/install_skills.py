"""Install the packaged skills without copying runtime data."""

import argparse
import os
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[1]
    destination = (
        args.destination or Path(os.getenv("CODEX_HOME", Path.home() / ".codex")) / "skills"
    )
    sources = sorted(p for p in (repository / "skills").iterdir() if (p / "SKILL.md").is_file())
    if not sources:
        raise RuntimeError("No packaged skills found")
    for source in sources:
        if (destination / source.name).exists() and not args.replace:
            raise FileExistsError(f"Inspect existing skill before --replace: {source.name}")
    for source in sources:
        for file in source.rglob("*"):
            if file.is_file() and file.suffix in {".md", ".json", ".yaml", ".py"}:
                output = destination / source.name / file.relative_to(source)
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, output)
        print(destination / source.name)


if __name__ == "__main__":
    main()
