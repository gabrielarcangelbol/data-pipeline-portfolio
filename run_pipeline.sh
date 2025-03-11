#!/bin/bash

# Directories
DEV_DIR="./dev"
PROD_DIR="./prod"
LOG_FILE="$DEV_DIR/data_pipeline.log"
CHANGELOG_FILE="$DEV_DIR/changelog.txt"

# Activate the virtual environment
source "C:/Users/gabri_7a484pu/Escritorio/code/DataEngineer_Codecademy/.venv/Scripts/activate"

# Create the production directory if it doesn't exist
if [ ! -d "$PROD_DIR" ]; then
    mkdir "$PROD_DIR"
    echo "Production directory created: $PROD_DIR"
else
    echo "Production directory already exists: $PROD_DIR"
fi

# Run the main Python script
echo "Running the main Python script."
python ./data_pipeline.py

# Check that the files have been created
if [ -f "$DEV_DIR/cademycode_clean_local.db" ] && [ -f "$DEV_DIR/cademycode_final_local.csv" ]; then
    echo "Files generated successfully."

    # Run the unit tests
    echo "Running the unit tests."
    python -m unittest ./test_data_pipeline.py

    # Check the logs for errors
    echo "Checking the logs for errors."
    if grep -q "ERROR" "$LOG_FILE"; then
        echo "Errors found in the log. Check $LOG_FILE for more details."
    else
        echo "No errors found in the log."

        # Check if there was an update in the changelog
        echo "Checking if there was an update in the changelog."
        if grep -q "Version" "$CHANGELOG_FILE"; then
            echo "Update detected. Moving files to production..."

            # Check that the files exist before moving them
            if [ -f "$DEV_DIR/cademycode_clean_local.db" ]; then
                echo "Moving cademycode_clean_local.db to production."
                mv $DEV_DIR/cademycode_clean_local.db $PROD_DIR/
                echo "File cademycode_clean_local.db moved to production."
            else
                echo "File cademycode_clean_local.db not found."
            fi

            if [ -f "$DEV_DIR/cademycode_final_local.csv" ]; then
                echo "Moving cademycode_final_local.csv to production."
                mv $DEV_DIR/cademycode_final_local.csv $PROD_DIR/
                echo "File cademycode_final_local.csv moved to production."
            else
                echo "File cademycode_final_local.csv not found."
            fi

            echo "Files moved to production."
        else
            echo "No updates detected in the changelog."
        fi
    fi
else
    echo "Expected files not generated. Check the main script."
fi