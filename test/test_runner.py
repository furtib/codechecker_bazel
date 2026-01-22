# Copyright 2023 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file runs tests.
For unittest pass `unit` as parameter
For FOSS tests pass `foss` as parameter
For verbosity use `-vvv`
To clean up FOSS test artifacts use `--clean`
To run the specified tests on all supported Bazel versions use `--all`
"""

import glob
import json
import shutil
import sys
import unittest
import argparse
from pathlib import Path

JSON_FILE = Path("../.github/bazel_version.json")
BAZELVERSION_FILE = Path("../.bazelversion")


def perform_system_clean():
    """
    Removes the test-proj folders from FOSS testing

    This function should not be necessary to re-run FOSS tests
    even if there was changes in the templates or init.sh files
    """
    print("Performing system cleanup (foss/*/test-proj)...")
    # Use glob to find all matching patterns
    targets = glob.glob("foss/*/test-proj")
    for target in targets:
        try:
            shutil.rmtree(target)
            print(f"Removed: {target}")
        except Exception as e:
            print(f"Failed to remove {target}: {e}")


def run_unittest_discovery(start_dir="unit", verbosity=1):
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern="test*.py")

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(
        description="Run unit tests across Bazel versions."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="The directory to explore for tests (e.g., 'unit' or 'tests/integration')",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run tests for all Bazel versions defined in the JSON file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        help="Increase verbosity (e.g., -v, -vv, -vvv)",
    )
    parser.add_argument(
        "--clean", action="store_true", help="Perform cleanup and exit."
    )

    args, unknown = parser.parse_known_args()

    # Cleanup
    if args.clean:
        perform_system_clean()
        sys.exit(0)

    if not args.directory:
        parser.error(
            "the following arguments are required: directory (unless using --clean)"
        )

    # Run with user set version
    if not args.all:
        success = run_unittest_discovery(
            start_dir=args.directory, verbosity=args.verbose
        )
        sys.exit(0 if success else 1)

    # Run on all supported versions
    original_content = None
    version_was_set = BAZELVERSION_FILE.exists()

    if version_was_set:
        original_content = BAZELVERSION_FILE.read_text()

    # To restore the contents of .bazelversion we wrap the test
    # in a try block, If the testing is interrupted, the file content
    # should still be restored.
    try:
        if not JSON_FILE.exists():
            print(f"Error: {JSON_FILE} not found.")
            sys.exit(1)

        with open(JSON_FILE, "r") as f:
            versions = json.load(f)

        overall_success = True
        for version in versions:
            print(f"\nTesting Bazel Version: {version}")
            print("=" * 80)

            BAZELVERSION_FILE.write_text(str(version))

            if not run_unittest_discovery(
                start_dir=args.directory, verbosity=args.verbose
            ):
                overall_success = False

            print("=" * 80)
        # Propagate test status for CI
        sys.exit(0 if overall_success else 1)

    finally:
        if version_was_set:
            BAZELVERSION_FILE.write_text(original_content)  # type: ignore
        elif BAZELVERSION_FILE.exists():
            BAZELVERSION_FILE.unlink()


if __name__ == "__main__":
    main()
