# cc_binary for simple C++ tests
load(
    "@rules_cc//cc:defs.bzl",
    "cc_binary",
    "cc_library",
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

load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)

cc_library(
    name = "target_with_both_extension",
    srcs = ["simple.c", "simple.cc"],
    tags = ["manual"],
)

compile_commands(
    name = "compile_commands_filter",
    targets = [
        ":target_with_both_extension",
    ],
)

code_checker_test(
    name = "code_checker_filter",
    targets = [
        "target_with_both_extension",
    ],
)
