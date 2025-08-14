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
Unit and functional tests
"""
import logging
import os
import re
import shlex
import subprocess
import sys
import unittest


class TestBase(unittest.TestCase):
    """Unittest base abstract class"""

    BAZEL_BIN_DIR = os.path.join("../../..", "bazel-bin", "test", "unit", "compile_flags")
    BAZEL_TESTLOGS_DIR = os.path.join("../../..", "bazel-testlogs", "test", "unit", "compile_flags")

    @classmethod
    def setUpClass(cls):
        """Load module, save environment"""
        # Save environment and location
        cls.save_env = os.environ
        cls.save_cwd = os.getcwd()
        # Move to test dir
        cls.test_dir = os.path.abspath(os.path.dirname(__file__))
        os.chdir(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        """Restore environment"""
        os.chdir(cls.save_cwd)
        os.environ = cls.save_env

    def setUp(self):
        """Before every test"""
        logging.debug("\n%s", "-" * 70)

    def check_command(self, cmd, exit_code=0):
        """Run shell command and check status"""
        logging.debug("Running: %s", cmd)
        commands = shlex.split(cmd)
        with subprocess.Popen(commands,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            stdout, stderr = process.communicate()
            self.assertEqual(
                process.returncode,
                exit_code, "\n" + "\n".join([
                    f"command: {cmd}",
                    f"stdout: {stdout.decode('utf-8')}",
                    f"stderr: {stderr.decode('utf-8')}"]))

    def grep_file(self, filename, regex):
        """Grep given filename"""
        pattern = re.compile(regex)
        logging.debug("RegEx = r'%s'", regex)
        with open(filename, "r", encoding="utf-8") as fileobj:
            for line in fileobj:
                if pattern.search(line):
                    logging.debug(line)
                    return True
        return False
        self.fail(f"Could not find r'{regex}' in '{filename}'")

class TestBasic(TestBase):
    """Basic tests"""

    def setUp(self):
        """Before every test: clean Bazel cache"""
        super().setUp()
        self.check_command("bazel clean")

    def test_bazel_test_compile_commands_cpp(self):
        """Test: bazel test ..."""
        self.check_command("bazel build "
                "//test/unit/compile_flags:compile_commands_cpp")
        compile_commands = os.path.join(
            self.BAZEL_BIN_DIR, "compile_commands_cpp",
            "compile_commands.json")
        if not self.grep_file(compile_commands, r"std=c++"):
            self.fail("No c++ flag on c++ file")

    def test_bazel_test_compile_commands_c(self):
        """Test: bazel test ..."""
        self.check_command("bazel build "
                "//test/unit/compile_flags:compile_commands_c")
        compile_commands = os.path.join(
            self.BAZEL_BIN_DIR, "compile_commands_c",
            "compile_commands.json")
        if self.grep_file(compile_commands, r"std=c++"):
            self.fail("C++ flag on c file")

    def test_bazel_test_code_checker_cpp(self):
        """Test: bazel test ..."""
        self.check_command("bazel build "
                "//test/unit/compile_flags:code_checker_cpp")
        compile_commands = os.path.join(
            self.BAZEL_BIN_DIR, "code_checker_cpp", "data",
            "compile_commands.json")
        if not self.grep_file(compile_commands, r"std=c++"):
            self.fail("No c++ flag on c++ file")

    def test_bazel_test_code_checker_c(self):
        """Test: bazel test ..."""
        self.check_command("bazel build "
                "//test/unit/compile_flags:code_checker_c")
        compile_commands = os.path.join(
            self.BAZEL_BIN_DIR, "code_checker_c", "data",
            "compile_commands.json")
        if self.grep_file(compile_commands, r"std=c++"):
            self.fail("C++ flag on c file")


def setup_logging():
    """Setup logging level for test execution"""
    # Enable debug logs for tests if "super verbose" flag is provided
    if "-vvv" in sys.argv:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[TEST] %(levelname)5s: %(message)s")


def main():
    """Run unittest"""
    setup_logging()
    logging.debug("Start testing...")
    unittest.main(buffer=True)


if __name__ == "__main__":
    main()
