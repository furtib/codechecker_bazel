# cc_binary for simple C++ tests
load(
    "@rules_cc//cc:defs.bzl",
    "cc_binary",
)

# codechecker rules
load(
    "@bazel_codechecker//src:codechecker.bzl",
    "codechecker_test",
)

# clang-tidy and clang -analyze rules
load(
    "@bazel_codechecker//src:clang.bzl",
    "clang_analyze_test",
    "clang_tidy_test",
)

# Prototype for CodeChecker analyze --file
load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)

# Simplest C++ test which should FAIL
cc_binary(
    name = "test_fail",
    srcs = ["faulty.cc"],
)

# And this clang-tidy test should fail
# Note "manual" tag (means should not be run with other tests)
clang_tidy_test(
    name = "clang_tidy_fail",
    tags = [
        "manual",
    ],
    targets = [
        "test_fail",
    ],
)

# And this clang -analyze test should fail
# Note "manual" tag (means should not be run with other tests)
clang_analyze_test(
    name = "clang_analyze_fail",
    tags = [
        "manual",
    ],
    targets = [
        "test_fail",
    ],
)

# This codechecker_test example supposed to fail showing findings report
# Note "manual" tag (means should not be run with other tests)
codechecker_test(
    name = "codechecker_fail",
    tags = [
        "manual",
    ],
    targets = [
        "test_fail",
    ],
)

code_checker_test(
    name = "code_checker_fail",
    tags = [
        "manual",
    ],
    targets = [
        "test_fail",
    ],
)