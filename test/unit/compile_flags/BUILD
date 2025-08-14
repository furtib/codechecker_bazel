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

# Prototype for CodeChecker analyze --file
# NOTE: CodeChecker analyze --file --ctu does not work
load(
    "@bazel_codechecker//src:code_checker.bzl",
    "code_checker_test",
)

# TODO: Apply custom cxx and conly flags to targets!
# may need to use toolchain or possibly:
# https://bazel.build/versions/7.6.0/rules/lib/toplevel/cc_common#compile)
# Note: The site changes a lot in version 6.5.0 (no flags I need)

cc_library(
    name = "c_target_with_cpp_flags",
    srcs = ["cpp_flags.c"],
    tags = ["manual"],
)

cc_library(
    name = "cpp_target_with_c_flags",
    srcs = ["c_flags.cc"],
    tags = ["manual"],
)

compile_commands(
    name = "compile_commands_c",
    targets = [
        ":c_target_with_cpp_flags",
    ],
)

compile_commands(
    name = "compile_commands_cpp",
    targets = [
        ":cpp_target_with_c_flags",
    ],
)

code_checker_test(
    name = "code_checker_cpp",
    targets = [
        "cpp_target_with_c_flags",
    ],
)

code_checker_test(
    name = "code_checker_c",
    targets = [
        "c_target_with_cpp_flags",
    ],
)
