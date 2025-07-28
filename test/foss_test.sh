#!/bin/bash
FOSS_BASE_DIR="./foss"
if [ ! -d "$FOSS_BASE_DIR" ]; then
    echo "Error: The directory '$FOSS_BASE_DIR' does not exist."
    exit 1
fi

if [ "$1" == "clean" ]; then
    find "$FOSS_BASE_DIR" -maxdepth 2 -mindepth 2 -type d -name "test-proj" ! -path "*/templates/*" -print -exec rm -rf {} +
    exit $?
fi

echo "Starting Bazel build process for projects in '$FOSS_BASE_DIR'..."
echo "-----------------------------------------------------------------"
find "$FOSS_BASE_DIR" -maxdepth 1 -mindepth 1 -type d | while read -r project_dir; do
    if ! command -v CodeChecker &> /dev/null; then
        echo "CodeChecker isn't available! Terminating..."
        echo "-----------------------------------------------------------------"
        exit 1
    fi
    project_name=$(basename "$project_dir")

    if [ "$project_name" == "templates" ]; then
        echo "Skipping 'templates' directory: $project_dir"
        continue
    fi

    echo ""
    echo "Processing project: $project_name ($project_dir)"
    echo "-----------------------------------------------------------------"

    pushd "$project_dir" > /dev/null || { echo "Error: Could not change to $project_dir. Skipping."; continue; }

    if [ ! -d "test-proj" ]; then
        echo "  Running ./init.sh..."
        if [ -f "./init.sh" ]; then
            ./init.sh > /dev/null
            if [ $? -ne 0 ]; then
                echo "  Warning: ./init.sh failed for $project_name. Skipping."; popd > /dev/null; continue;
            fi
        else
            echo "  Warning: ./init.sh not found in $project_name. Skipping."; popd > /dev/null; continue;
        fi
    else
        echo "test-proj already exists. Skipping init.sh for $project_name"
    fi

    if [ -d "test-proj" ]; then
        pushd "test-proj" > /dev/null || { echo "Error: Could not change to test-proj in $project_name. Skipping."; popd > /dev/null; continue; }

        echo "  Running bazel build :codechecker_test..."
        bazel build :codechecker_test
        if [ $? -ne 0 ]; then
            echo "  Error: 'bazel build :codechecker_test' failed for $project_name. Check logs above."
        fi

        echo "  Running bazel build :code_checker_test..."
        bazel build :code_checker_test
        if [ $? -ne 0 ]; then
            echo "  Error: 'bazel build :code_checker_test' failed for $project_name. Check logs above."
        fi

        popd > /dev/null
    else
        echo "  Error: 'test-proj' directory not found in $project_name. Skipping Bazel builds."
    fi

    popd > /dev/null

    echo "-----------------------------------------------------------------"
    echo "Finished processing project: $project_name"
done

echo ""
echo "-----------------------------------------------------------------"
echo "Bazel build process completed."
