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
This script replaces the content of the .bazelversion file
from .github/bazel_version.json and runs the equivalent of
python3 -m unittest discover @a
For unittest pass `unit` as parameter
For FOSS tests pass `foss` as parameter #TODO: Add cleanup between FOSS runs
For verbosity use `-vvv`
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


def run_unittest_discovery(start_dir="unit", verbosity=1):
    """
    The equivalent of python3 -m unittest discover $start_dir
    
    :param start_dir: The directory in which it searches for tests
    :param verbosity: How verbose the output should be
    """
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(
        description="Run unit tests across Bazel versions."
    )
    parser.add_argument(
        "directory",
        help="The directory to explore for tests (e.g., 'unit' or 'tests/integration')",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=1,
        help="Increase verbosity (e.g., -v, -vv, -vvv)",
    )

    args, unknown = parser.parse_known_args()

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
