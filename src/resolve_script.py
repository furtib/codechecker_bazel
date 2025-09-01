#!{PythonPath}
"""
CodeChecker Bazel build & test wrapper script
"""

from __future__ import print_function
import getpass
import logging
import multiprocessing
import os
import plistlib
import re
import shlex
import socket
import subprocess
import sys
from time import sleep

BAZEL_PATHS = {
    # Running with Build Barn produces path output like:
    # /worker/build/b301eed7f2bf2fd8/root/local_path.cc
    # By removing the part until bin we have resolved the path to a local file 
    r"\/worker\/build\/[0-9a-fA-F]{16}\/root\/": "",
    # Sometimes the previous part is followed by this, before the local_path:
    #r"bazel-out\/k8-fastbuild\/bin\/": "",
    # Virtual includes seems to be just a folder between the package and the
    # folder containing the header files, like this:
    # /path/to/package/_virtual_include/folder_with_headers/header.h
    #r"\/_virtual_includes\/" : "/",
}

EXECUTION_MODE = "{Mode}"
VERBOSITY = "{Verbosity}"
CODECHECKER_PATH = "/venv/bin/CodeChecker"
CODECHECKER_SKIPFILE = "{codechecker_skipfile}"
CODECHECKER_CONFIG = "{codechecker_config}"
CODECHECKER_ANALYZE = "{codechecker_analyze}"
CODECHECKER_FILES = "{codechecker_files}"
CODECHECKER_OLD_FILES = "{codechecker_old_files}"
CODECHECKER_LOG = "{codechecker_log}"
CODECHECKER_SEVERITIES = "{Severities}"
CODECHECKER_ENV = "{codechecker_env}"
COMPILE_COMMANDS = "{compile_commands}"

def fix_bazel_paths():
    """ Remove Bazel leading paths in all files """
    stage("Fix CodeChecker output:")
    folder = CODECHECKER_OLD_FILES
    logging.info("Fixing Bazel paths in %s", folder)
    counter = 0
    for root, _, files in os.walk(folder):
        for filename in files:
            fullpath = os.path.join(root, filename)
            newpath = os.path.join(CODECHECKER_FILES, filename)
            with open(fullpath, "rt") as data_file:
                data = data_file.read()
                for pattern, replace in BAZEL_PATHS.items():
                    data = re.sub(pattern, replace, data)
            with open(newpath, "w") as data_file:
                data_file.write(data)
            counter += 1
    logging.info("Fixed Bazel paths in %d files", counter)


def realpath(filename):
    """ Return real full absolute path for given filename """
    if os.path.exists(filename):
        real_file_name = os.path.abspath(os.path.realpath(filename))
        logging.debug("Updating %s -> %s", filename, real_file_name)
        filename = real_file_name
    return filename


def resolve_plist_symlinks(filepath, newpath):
    """ Resolve the symbolic links in plist files to real file paths """
    logging.info("Processing plist file: %s", filepath)
    if sys.version_info >= (3, 9):
        with open(filepath, "rb") as input_file:
            file_contents = plistlib.load(input_file)
    else:
        file_contents = plistlib.readPlist(filepath)
    if file_contents["files"]:
        final_files = []
        for entry in file_contents["files"]:
            final_files.append(realpath(entry))
        file_contents["files"] = final_files
        with open(newpath, "wb") as output_file:
            if sys.version_info >= (3, 9):
                plistlib.dump(file_contents, output_file)
            else:
                plistlib.writePlist(file_contents, output_file)


def resolve_yaml_symlinks(filepath, newpath):
    """ Resolve the symbolic links in YAML files to real file paths """
    logging.info("Processing YAML file: %s", filepath)
    fields = [
        r"MainSourceFile:\s*",
        r"\s*-? FilePath:\s*",
    ]
    updated = 0
    line_to_write = []
    with open(filepath, "r") as input_file:
        for line in input_file.readlines():
            for field in fields:
                pattern = "(%s)'(.*)'" % field
                match = re.match(pattern, line)
                if match:
                    field = match.group(1)
                    filename = match.group(2)
                    fullpath = realpath(filename)
                    if fullpath != filename:
                        updated += 1
                        replace = field + "'" + fullpath + "'\r\n"
                        line = replace
                    break
            line_to_write.append(line)
    if updated:
        logging.debug("     %d updated paths", updated)
        with open(newpath, "w") as output_file:
            logging.debug("     saving...")
            output_file.writelines(line_to_write)

def separator(method="info"):
    """ Print log separator line to logging.info() or other logging methods """
    getattr(logging, method)("#" * 23)

def stage(title, method="info"):
    """ Print stage title into log """
    separator(method)
    getattr(logging, method)("### " + title)
    separator(method)


def resolve_symlinks():
    """ Change ".../execroot/apps" paths to absolute paths in data/* files """
    stage("Resolve file paths in CodeChecker analyze output:")
    analyze_outdir = CODECHECKER_FILES
    logging.info("Resolving file paths in CodeChecker analyze output at: %s", analyze_outdir)
    files_processed = 0
    for root, _, files in os.walk(analyze_outdir):
        for filename in files:
            filepath = os.path.join(root, filename)
            newpath = os.path.join(CODECHECKER_FILES, filename)
            if os.path.splitext(filepath)[1] == ".plist":
                resolve_plist_symlinks(filepath, newpath)
            elif os.path.splitext(filepath)[1] == ".yaml":
                resolve_yaml_symlinks(filepath, newpath)
            files_processed += 1
    logging.info("Processed file paths in %d files", files_processed)

def update_file_paths():
    """ Resolve symlinks from local jobs, then try fixing path from remote executors """
    fix_bazel_paths()
    resolve_symlinks()


def main():
    """ Main function """
    update_file_paths()


if __name__ == "__main__":
    main()
