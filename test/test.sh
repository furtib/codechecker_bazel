#!/bin/bash

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

JSON_FILE="../.github/bazel_version.json"
BAZELVERSION_FILE="../.bazelversion"
VERSION_WAS_SET=false
ORIGINAL_CONTENT=""

RUN_MULTI_VERSION=false
NEW_ARGS=()

for arg in "$@"; do
    if [[ "$arg" == "--all" ]]; then
        RUN_MULTI_VERSION=true
    else
        NEW_ARGS+=("$arg")
    fi
done
set -- "${NEW_ARGS[@]}"

if [ "$RUN_MULTI_VERSION" = true ]; then
    if [ -f "$BAZELVERSION_FILE" ]; then
        ORIGINAL_CONTENT=$(cat "$BAZELVERSION_FILE")
        VERSION_WAS_SET=true
    fi

    cleanup() {
        if [ "$VERSION_WAS_SET" = true ]; then
            echo "$ORIGINAL_CONTENT" > "$BAZELVERSION_FILE"
        else
            rm -f "$BAZELVERSION_FILE"
        fi
    }
    trap cleanup EXIT

    jq -rc '.[]' "$JSON_FILE" | while read -r element; do
        echo "Bazel: $element"
        echo "------------------------------------"
        echo $element > "$BAZELVERSION_FILE"
        python3 -m unittest discover unit "$@"
        echo "------------------------------------"

    done
else
    python3 -m unittest discover unit "$@"
fi
