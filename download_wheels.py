#!/usr/bin/env python3
"""Download every wheel for a specific version of a PyPI package."""

import argparse
import sys
from pathlib import Path
from urllib.request import urlretrieve, urlopen
import json


def get_wheels(project: str, version: str) -> list[dict]:
    url = f"https://pypi.org/pypi/{project}/{version}/json"
    try:
        with urlopen(url) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        sys.exit(f"Failed to fetch metadata: {e}")

    return [f for f in data["urls"] if f["filename"].endswith(".whl")]


def download_wheels(project: str, version: str):
    wheels = get_wheels(project, version)

    if not wheels:
        sys.exit(f"No wheels found for {project}=={version}")

    dest = Path(f"{project}/{version}")

    dest.mkdir(parents=True, exist_ok=True)
    print(f"Found {len(wheels)} wheel(s) for {project}=={version}\n")

    for i, whl in enumerate(wheels, 1):
        filename = whl["filename"]
        target = dest / filename
        size_mb = whl["size"] / 1_000_000

        if target.exists():
            print(f"  [{i}/{len(wheels)}] {filename} (already exists, skipping)")
            continue

        print(f"  [{i}/{len(wheels)}] {filename} ({size_mb:.1f} MB)")
        urlretrieve(whl["url"], target)

    print(f"\nDone. Wheels saved to {dest.resolve()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="PyPI project name")
    parser.add_argument("version", help="Version to download")
    args = parser.parse_args()
    download_wheels(args.project, args.version)


if __name__ == "__main__":
    main()
