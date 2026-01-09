load(
    "@default_codechecker_tools//:defs.bzl",
    "BAZEL_VERSION"
)

def old_bazel_attributes():
    if BAZEL_VERSION.split(".")[0] in "0123456":
        return ({"_whitelist_function_transition": attr.label(
        default = "@bazel_tools//tools/whitelists/function_transition_whitelist",
        doc = "needed for transitions",
        )})
    return {}
