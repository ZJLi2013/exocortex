"""Mirror hand-maintained trackers into raw/ as read-only snapshots."""

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
GITHUB = ROOT.parents[1]

# name -> (source dir relative to GITHUB, entries under it; directories are copied recursively)
SOURCES = {
    "robotrsi": ("ji_qi_ren/robot_rl_from_zero_to_expert/robotRSI/doc", ["landscape.md", "works"]),
    "agent_loop": ("ai_agents/agent-loop/docs/study", ["research-rsi-track.md"]),
}


def expected_files(src: Path, entries: list[str]) -> dict[str, Path]:
    files = {}
    for entry in entries:
        path = src / entry
        if path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.is_file():
                    files[f.relative_to(src).as_posix()] = f
        else:
            files[entry] = path
    return files


def raw_files(dst: Path) -> set[str]:
    if not dst.exists():
        return set()
    return {f.relative_to(dst).as_posix() for f in dst.rglob("*") if f.is_file()}


def git(src: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(src), *args], capture_output=True, text=True, check=True).stdout.strip()


def manifest() -> str:
    rows = ["# raw manifest", "", "由 `scripts/sync_sources.py` 生成，不要手改。", "",
            "| 源 | 路径 | 源 commit | 文件数 | 未提交改动 |", "|---|---|---|---|---|"]
    for name, (rel, entries) in SOURCES.items():
        src = GITHUB / rel
        commit = git(src, "log", "-1", "--format=%h", "--", *entries) or "未提交"
        dirty = "有" if git(src, "status", "--porcelain", "--", *entries) else "无"
        rows.append(f"| {name} | {rel} | {commit} | {len(expected_files(src, entries))} | {dirty} |")
    return "\n".join(rows) + "\n"


def sync() -> None:
    for name, (rel, entries) in SOURCES.items():
        dst = RAW / name
        files = expected_files(GITHUB / rel, entries)
        for stale in raw_files(dst) - files.keys():
            (dst / stale).unlink()
        for relpath, src_file in files.items():
            target = dst / relpath
            if not target.exists() or not filecmp.cmp(src_file, target, shallow=False):
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src_file, target)
        print(f"{name}: {len(files)} files")
    (RAW / "manifest.md").write_text(manifest(), encoding="utf-8", newline="\n")


def check() -> bool:
    ok = True
    for name, (rel, entries) in SOURCES.items():
        dst = RAW / name
        files = expected_files(GITHUB / rel, entries)
        problems = [f"missing {p}" for p in files.keys() - raw_files(dst)]
        problems += [f"stale {p}" for p in raw_files(dst) - files.keys()]
        problems += [f"differs {p}" for p, f in files.items()
                     if (dst / p).exists() and not filecmp.cmp(f, dst / p, shallow=False)]
        print(f"{name}: {len(files)} files, " + ("ok" if not problems else "; ".join(sorted(problems))))
        ok &= not problems
    manifest_path = RAW / "manifest.md"
    manifest_ok = manifest_path.exists() and manifest_path.read_text(encoding="utf-8") == manifest()
    print("manifest: " + ("ok" if manifest_ok else "out of date"))
    return ok and manifest_ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify raw/ mirrors sources; exit 1 otherwise")
    args = parser.parse_args()
    if args.check:
        sys.exit(0 if check() else 1)
    sync()


if __name__ == "__main__":
    main()
