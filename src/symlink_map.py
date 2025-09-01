#!/usr/bin/env python3
import os
import sys
import json

def build_symlink_map(root_dir: str) -> dict:
    """
    Walks through root_dir recursively, finds all symlinks,
    and maps them to their real target paths.
    """
    symlink_map = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                try:
                    # Resolve the absolute, normalized target path
                    target = os.path.realpath(path)
                    symlink_map[path] = target
                except OSError as e:
                    # Handle broken symlinks gracefully
                    symlink_map[path] = f"<broken: {e}>"

        # Also check symlinked directories
        #for name in os.listdir(dirpath):
        #    path = os.path.join(dirpath, name)
        #    if os.path.islink(path) and os.path.isdir(path):
        #        try:
        #            target = os.path.realpath(path)
        #            symlink_map[path] = target
        #        except OSError as e:
        #            symlink_map[path] = f"<broken: {e}>"

    return symlink_map


def main():
    root_dir = "{root}"
    output = "{output}"
    print("HELLO!", file=sys.stderr)
    if not os.path.exists(root_dir):
        print(f"Error: Directory {root_dir} does not exist", file=sys.stderr)

    symlink_map = build_symlink_map(root_dir)

    # Pretty-print the dictionary as JSON
    print(json.dumps(symlink_map, indent=2), file=sys.stderr)

    try:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(symlink_map, f, indent=2, ensure_ascii=False)
        print(f"✅ Symlink map successfully written to: {output}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Failed to write to {output}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
