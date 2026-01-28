load("@bazel_skylib//lib:unittest.bzl", "analysistest", "asserts")
load("compile_commands.bzl", "SourceFilesInfo")
load(":per_file.bzl", "testing_only_collect_all_sources_and_headers")

# This is a mock cc_binary rule
def _mock_source_rule_impl(ctx):
    return [
        CcInfo(),  # May need more info depending on bazel version, works under bazel 6
        SourceFilesInfo(
            transitive_source_files = depset(ctx.files.srcs),
            headers = depset([depset(ctx.files.hdrs)]),
        ),
    ]

mock_source_rule = rule(
    implementation = _mock_source_rule_impl,
    attrs = {
        "srcs": attr.label_list(allow_files = True),
        "hdrs": attr.label_list(allow_files = True),
    },
)

# This is a mock per_file_test rule
# This provider is the "return value" of the "test"
FileResultInfo = provider(fields = ["files"])

def _subject_rule_impl(ctx):
    files = testing_only_collect_all_sources_and_headers(ctx)
    return [FileResultInfo(files = files)]

subject_rule = rule(
    implementation = _subject_rule_impl,
    attrs = {"targets": attr.label_list()},
)

# The actual test

def _collect_files_test_impl(ctx):
    env = analysistest.begin(ctx)
    target_under_test = analysistest.target_under_test(env)

    # We use the results in the provider to assert on, this is to be able to pass results between rules.
    collected_files = target_under_test[FileResultInfo].files
    filenames = [f.basename for f in collected_files]

    asserts.true(env, "main.cc" in filenames)
    asserts.true(env, "lib.h" in filenames)
    asserts.equals(env, 2, len(filenames))

    return analysistest.end(env)

# Rule factory using the _collect_files_test_impl as implementation
collect_files_test = analysistest.make(_collect_files_test_impl)  # place expect failure here

def test_collect_sources():
    # creates an instance of the mock cc_binary/library rule.
    # We could create this by hand in the build file
    mock_source_rule(name = "mock_target", srcs = ["main.cc"], hdrs = ["lib.h"])

    # create an instance of the per_file_test mock rule
    # We could create this in the BUILD file
    subject_rule(name = "subject", targets = [":mock_target"])

    # Instance of the rule created by the rule_factory
    collect_files_test(name = "collect_files_test", target_under_test = ":subject")
