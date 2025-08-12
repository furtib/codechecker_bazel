# cc_binary for simple C++ tests
load(
    "@rules_cc//cc:defs.bzl",
    "cc_binary",
)

# compile_commands rule
load(
    "@bazel_codechecker//src:compile_commands.bzl",
    "compile_commands",
)

# codechecker rules
load(
    "@bazel_codechecker//src:codechecker.bzl",
    "codechecker",
    "codechecker_config",
    "codechecker_suite",
    "codechecker_test",
)

# clang-tidy and clang -analyze rules
load(
    "@bazel_codechecker//src:clang.bzl",
    "clang_analyze_test",
    "clang_tidy_test",
)

# clang -analyze + CTU rule
load(
    "@bazel_codechecker//src:clang_ctu.bzl",
    "clang_ctu_test",
)

# Prototype for CodeChecker analyze --file
load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)

# Simplest C++ test which should PASS
cc_binary(
    name = "test_pass",
    srcs = ["simple.cc"],
)

# Generate compile_commands.json file for host test
compile_commands(
    name = "compile_commands_pass",
    targets = [
        ":test_pass",
    ],
)

# This simple clang-tidy test should pass
clang_tidy_test(
    name = "clang_tidy_pass",
    targets = [
        "test_pass",
    ],
)

# This simple clang -analyze test should pass
clang_analyze_test(
    name = "clang_analyze_pass",
    options = [
        "-fno-color-diagnostics",  # Example
        # "-Xanalyzer -analyzer-disable-all-checks",
    ],
    targets = [
        "test_pass",
    ],
)

# This simple clang -analyze + CTU test should pass
clang_ctu_test(
    name = "clang_ctu_pass",
    targets = [
        "test_pass",
    ],
)

# CodeChecker configuration file in JSON format
filegroup(
    name = "codechecker_config_file",
    srcs = [":config.json"],
)

# CodeChecker configuration options specification
# using JSON configuration file based approach,
# inherently supported by CodeChecker
# TODO: isolate to other test
codechecker_config(
    name = "codechecker_config_json",
    config_file = "codechecker_config_file",
)

# Simple codechecker rule - performs only "build" phase without "test"
codechecker(
    name = "codechecker_pass_build",
    config = "codechecker_config_json",
    targets = [
        "test_pass",
    ],
)

# Simplest codechecker_test example
# Runs CodeChecker on "test_pass" target
codechecker_test(
    name = "codechecker_pass",
    config = "codechecker_config_json",
    targets = [
        "test_pass",
    ],
)

# Simplest codechecker_suite example for "test_pass"
# Can run CodeChecker on targets built for different platforms
# This example performs build for just default platform i.e gcc
# FIXME
codechecker_suite(
    name = "codechecker_pass_multi",
    config = "codechecker_config_json",
    # platforms = [
    #     "@platforms//os:linux",
    #     "@platforms//os:ios",
    #     "@platforms//os:android",
    # ],
    targets = [
        "test_pass",
    ],
)

code_checker_test(
    name = "code_checker_pass",
    targets = [
        "test_pass",
    ],
)
