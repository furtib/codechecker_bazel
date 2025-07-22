#!/bin/bash

git clone --recurse https://github.com/madler/zlib.git test-proj
cd test-proj
git checkout 5a82f71ed1dfc0bec044d9702463dbdf84ea3b71

# This file must be in the root of the project to be analyzed for bazelisk to work
cp ../.bazelversion ./.bazelversion

echo '#-------------------------------------------------------

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
    name = "codechecker_test",
    targets = [
        ":z",
    ],
)

code_checker_test(
    name = "code_checker_test",
    targets = [
        ":z",
    ],
)

#-------------------------------------------------------' >> BUILD.bazel

echo '#----------------------------------------------------

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "bazel_codechecker",
    remote = "https://github.com/Ericsson/codechecker_bazel.git",
    branch = "main",
)

load(
    "@bazel_codechecker//src:tools.bzl",
    "register_default_codechecker",
    "register_default_python_toolchain",
)

register_default_python_toolchain()

register_default_codechecker()

#----------------------------------------------------' >> WORKSPACE
