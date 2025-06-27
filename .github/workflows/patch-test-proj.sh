#!/bin/bash

FORK_REPO="$1"
FORK_BRANCH="$2"

git clone --recurse https://github.com/jbeder/yaml-cpp.git
cd yaml-cpp
git checkout yaml-cpp-0.7.0

# Specify bazel version for bazelisk
echo "6.5.0" > .bazelversion

# Add codechecker to the project
cat <<EOF >> BUILD.bazel
#-------------------------------------------------------

# codechecker rules
load(
    "@bazel_codechecker//src:codechecker.bzl",
    "codechecker_test",
)
load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)


codechecker_test(
    name = "codechecker_test_yaml-cpp",
    targets = [
        ":yaml-cpp",
    ],
)

code_checker_test(
    name = "code_checker_test_yaml-cpp",
    targets = [
        ":yaml-cpp",
    ],
)

#-------------------------------------------------------
EOF

cat <<EOF >> WORKSPACE
#----------------------------------------------------

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "bazel_codechecker",
    remote = "https://github.com/${FORK_REPO}",
    branch = "${FORK_BRANCH}",
)

load(
    "@bazel_codechecker//src:tools.bzl",
    "register_default_codechecker",
    "register_default_python_toolchain",
)

register_default_python_toolchain()

register_default_codechecker()

#----------------------------------------------------
EOF