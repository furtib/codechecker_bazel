# cc_binary for simple C++ tests
load(
    "@rules_cc//cc:defs.bzl",
    "cc_library",
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

# Test defect in CTU mode
cc_library(
    name = "test_ctu",
    hdrs = ["header.h"],
    srcs = [
        "file1.cc",
        "file2.cc",
    ],
)

# And this clang -analyze + CTU test should fail
# Note "manual" tag (means should not be run with other tests)
clang_ctu_test(
    name = "clang_ctu_fail",
    options = [
        # "-fno-color-diagnostics",  # Example
        # "-Xanalyzer -analyzer-disable-all-checks",
    ],
    tags = [
        "manual",
    ],
    targets = [
        "test_ctu",
    ],
)

# Simple pef-file Codechecker CTU test should fail
# Note "manual" tag (means should not be run with other tests)
code_checker_test(
    name = "code_checker_ctu",
    options = [
        "--ctu",
    ],
    tags = [
        "manual",
    ],
    targets = [
        "test_ctu",
    ],
)
