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
Unit test for CTU actions
"""
import os
import shutil
import unittest
from typing import final
from common.base import TestBase


class TestTemplate(TestBase):
    """TODO: Add a description"""

    # Set working directory
    __test_path__ = os.path.dirname(os.path.abspath(__file__))
    # TODO: fix folder name
    BAZEL_BIN_DIR = os.path.join("../../..", "bazel-bin", "test", "unit", "ctu")
    BAZEL_TESTLOGS_DIR = os.path.join(
        "../../..", "bazel-testlogs", "test", "unit", "ctu"
    )

    @final
    @classmethod
    def setUpClass(cls):
        """TODO: Define set up before the test suite"""
        super().setUpClass()
        cls.run_command("bazel clean")

    def test_code_checker_ctu_caching_disabled(self):
        """Test: bazel build"""
        try:
            # This setup is only needed for this single test
            os.mkdir("tmp")
            shutil.copy("first.cc", "tmp")
            shutil.copy("zero.cc", "tmp")
            shutil.copy("link.h", "tmp")
            shutil.copy("BUILD", "tmp")

            target = "//test/unit/ctu/tmp:code_checker_ctu"
            ret, _, _ = self.run_command(
                f"bazel test {target}"
            )
            self.assertEqual(ret, 3)
            try:
                with open("tmp/zero.cc", "a", encoding="utf-8") as f:
                    f.write("//test")
            except FileNotFoundError:
                self.fail(f"File not found!")
            ret, _, stderr = self.run_command(
                f"bazel test {target} --subcommands"
            )
            self.assertEqual(ret, 3)
            self.assertEqual(
                stderr.count(f"SUBCOMMAND: # {target} [action 'CodeChecker"), 2
            )
        finally:
            # Cleanup specific to this test
            try:
                shutil.rmtree("tmp")
            except FileNotFoundError:
                self.fail("Temporary working directory does not exists!")
        


if __name__ == "__main__":
    unittest.main(buffer=True)
