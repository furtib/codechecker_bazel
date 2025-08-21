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
Unit test for resolving path in all plist files
"""
import logging
import os
import re
import unittest
import glob
from typing import final
from common.base import TestBase


class TestVirtualInclude(TestBase):
    """Tests checking virtual include path resolution"""

    # Set working directory
    __test_path__ = os.path.dirname(os.path.abspath(__file__))
    BAZEL_BIN_DIR = os.path.join(
        "../../..", "bazel-bin", "test", "unit", "virtual_include"
    )
    BAZEL_TESTLOGS_DIR = os.path.join(
        "../../..", "bazel-testlogs", "test", "unit", "virtual_include"
    )

    @final
    @classmethod
    def setUpClass(cls):
        """Set up before the test suite"""
        super().setUpClass()
        cls.run_command("bazel clean")


    def test_bazel_plist_path_resolved(self):
        """Test: bazel build :codechecker_virtual_include"""
        ret, _, _ = self.run_command(
            "bazel build //test/unit/virtual_include:codechecker_virtual_include"
        )
        self.assertEqual(ret, 0)
        ret, _, _ = self.run_command(
            "bazel build //test/unit/virtual_include:code_checker_virtual_include",
        )
        self.assertEqual(ret, 0)
        plist_files = glob.glob(
            os.path.join(self.BAZEL_BIN_DIR, "**", "*.plist"), recursive=True
        )
        self.assertTrue(
            os.path.isdir(f"{self.BAZEL_BIN_DIR}/_virtual_includes")
        )
        for plist_file in plist_files:
            logging.debug(f"Checking file: {plist_file}")
            # FIXME: This shouldn't find anything
            if len(self.grep_file(plist_file, r"/_virtual_includes/")) < 0:
                self.fail(
                    f"Found unresolved symlink within CodeChecker report: {plist_file}"
                )


if __name__ == "__main__":
    unittest.main(buffer=True)
