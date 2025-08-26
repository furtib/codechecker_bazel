# cc_binary for simple C++ tests
load(
    "@rules_cc//cc:defs.bzl",
    "cc_library",
)

# codechecker rules
load(
    "@bazel_codechecker//src:codechecker.bzl",
    "codechecker_test",
)

# clang -analyze + CTU rule
load(
    "@bazel_codechecker//src:clang_ctu.bzl",
    "clang_ctu_test",
)

# Prototype for CodeChecker analyze --file
# NOTE: CodeChecker analyze --file --ctu does not work
load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)

# Test defect in CTU mode
cc_library(
    name = "test_ctu",
    hdrs = ["link.h"],
    srcs = [
        "first.cc",
        "zero.cc",
        ],
)

# Test no defects in CTU mode
cc_library(
    name = "test_ctu_no_find",
    hdrs = ["link.h"],
    srcs = [
        "first.cc",
        "one.cc",
        ],
)


# This codechecker_test CTU example supposed to fail showing findings report
# Note "manual" tag (means should not be run with other tests)
codechecker_test(
    name = "codechecker_ctu",
    analyze = [
        "--ctu",
    ],
    tags = [
        "manual",
    ],
    targets = [
        "test_ctu",
    ],
)

# This simple clang -analyze + CTU test should pass
clang_ctu_test(
    name = "clang_ctu_pass",
    targets = [
        "test_ctu_no_find",
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
