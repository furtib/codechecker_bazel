#!/bin/bash
JSON_FILE="../.github/bazel_version.json"
BAZELVERSION_FILE="../.bazelversion"
VERSION_WAS_SET=false
ORIGINAL_CONTENT=""

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
    python3 -m unittest discover foss "$@"
    echo "------------------------------------"

done
