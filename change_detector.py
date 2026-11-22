import argparse
import json
import subprocess
from pathlib import Path


def run_git_command(repo_path, *args):
    result = subprocess.run(
        ["git", "-C", str(repo_path), *args],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def get_changed_files(repo_path, base_commit, head_commit):
    output = run_git_command(
        repo_path,
        "diff",
        "--name-status",
        "-M",
        base_commit,
        head_commit
    )

    changed_files = []

    for line in output.splitlines():
        parts = line.split("\t")

        status_code = parts[0]

        if status_code == "A":
            changed_files.append({
                "file": parts[1],
                "status": "added"
            })

        elif status_code == "M":
            changed_files.append({
                "file": parts[1],
                "status": "modified"
            })

        elif status_code == "D":
            changed_files.append({
                "file": parts[1],
                "status": "deleted"
            })

        elif status_code.startswith("R"):
            changed_files.append({
                "file": parts[2],
                "status": "renamed",
                "old_file": parts[1]
            })

    return changed_files


def generate_summary(changed_files):
    summary = {
        "modified": 0,
        "added": 0,
        "deleted": 0,
        "renamed": 0
    }

    for file in changed_files:
        status = file["status"]

        if status in summary:
            summary[status] += 1

    return summary


def generate_report(repo_path, base_commit, head_commit):
    changed_files = get_changed_files(
        repo_path,
        base_commit,
        head_commit
    )

    report = {
        "repository": Path(repo_path).name,
        "base_commit": base_commit,
        "head_commit": head_commit,
        "changed_files": changed_files,
        "summary": generate_summary(changed_files)
    }

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Detect changed files between Git revisions."
    )

    parser.add_argument(
        "--repo",
        default=".",
        help="Path to Git repository"
    )

    parser.add_argument(
        "--base",
        required=True,
        help="Base commit SHA"
    )

    parser.add_argument(
        "--head",
        default="HEAD",
        help="Head commit SHA (default: HEAD)"
    )

    parser.add_argument(
        "--output",
        default="change_report.json",
        help="Output JSON file"
    )

    args = parser.parse_args()

    repo_path = Path(args.repo).resolve()

    report = generate_report(
        repo_path,
        args.base,
        args.head
    )

    output_path = Path(args.output).resolve()

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Change detection completed.")
    print(f"Modified: {report['summary']['modified']}")
    print(f"Added: {report['summary']['added']}")
    print(f"Deleted: {report['summary']['deleted']}")
    print(f"Renamed: {report['summary']['renamed']}")
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()