# Copyright 2023 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def get_config_file(ctx):
    """
    Returns (config_file, environment_variables)
    config_file is a file object that is readable during Codechecker execution
    """
    config_file_name = ctx.attr.name + "/config.json"
    ctx_config_file = ctx.actions.declare_file(config_file_name)

    # Create CodeChecker JSON config file and env vars
    if ctx.attr.config:
        if type(ctx.attr.config) == "list":
            config_info = ctx.attr.config[0][CodeCheckerConfigInfo]
        else:
            config_info = ctx.attr.config[CodeCheckerConfigInfo]
        if config_info.config_file:
            # Create a copy of CodeChecker configuration file
            # provided via codechecker_config(config_file)
            config_file = config_info.config_file.files.to_list()[0]
            ctx.actions.run(
                inputs = [config_file],
                outputs = [ctx_config_file],
                mnemonic = "CopyFile",
                progress_message = "Copying CodeChecker config file",
                executable = "cp",
                arguments = [
                    config_file.path,
                    ctx_config_file.path,
                ],
            )
        else:
            # Create CodeChecker configuration file in JSON format
            # from Bazel codechecker_config(analyze, parse)
            config_json = {}
            if config_info.analyze:
                config_json["analyze"] = config_info.analyze
            if config_info.parse:
                config_json["parse"] = config_info.parse
            config_content = json.encode_indent(config_json)
            ctx.actions.write(
                output = ctx_config_file,
                content = config_content,
                is_executable = False,
            )

        # Pack env vars for CodeChecker
        codechecker_env = "; ".join(config_info.env)
    else:
        # Empty CodeChecker JSON config file
        ctx.actions.write(
            output = ctx_config_file,
            content = "{}",
            is_executable = False,
        )
        codechecker_env = ""
    return (ctx_config_file, codechecker_env)

CodeCheckerConfigInfo = provider(
    doc = "Defines CodeChecker configuration",
    fields = {
        "analyze": "List of arguments for CodeChecker analyze command",
        "parse": "List of arguments for CodeChecker parse command",
        "config_file": "CodeChecker configuration file in JSON format",
        "env": "Environment variables for CodeChecker",
    },
)

def _codechecker_config_impl(ctx):
    return [
        CodeCheckerConfigInfo(
            analyze = ctx.attr.analyze,
            parse = ctx.attr.parse,
            config_file = ctx.attr.config_file,
            env = ctx.attr.env,
        ),
    ]

codechecker_config = rule(
    implementation = _codechecker_config_impl,
    attrs = {
        "analyze": attr.string_list(
            default = [],
            doc = "List of arguments for CodeChecker analyze command",
        ),
        "parse": attr.string_list(
            default = [],
            doc = "List of arguments for CodeChecker parse command",
        ),
        "config_file": attr.label(
            default = None,
            allow_single_file = True,
        ),
        "env": attr.string_list(
            default = [],
            doc = "List of environment variables for CodeChecker",
        ),
    },
)
