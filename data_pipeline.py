import os
import pandas as pd
from sqlalchemy import create_engine
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='dev/data_pipeline.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def update_changelog(new_rows, missing_data_counts):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('dev/changelog.txt', 'a') as f:
        f.write(f"## [{timestamp}]\n")
        f.write(f"### Added\n")
        f.write(f"- New rows added: {new_rows}\n")
        f.write(f"- Missing data counts: {missing_data_counts}\n")
        f.write(f"### Fixed\n")
        f.write(f"- Fixed missing table errors for `cademycode_courses`\n")
        f.write(f"### Changed\n")
        f.write(f"- Combined tables into `cademycode_final_local`\n\n")

def save_current_row_count(row_count):
    # Save the current row count to a file for future comparisons
    with open('dev/previous_row_count.txt', 'w') as file:
        file.write(str(row_count))

def main():
    try:
        # Ensure the directory exists
        os.makedirs('dev', exist_ok=True)

        # Establish the database connection to SQLite
        engine = create_engine('sqlite:///dev/cademycode_updated.db')

        # Read cleaned data from the database
        logging.info("Reading data from the database.")
        df_courses = pd.read_sql_query('SELECT * FROM cademycode_courses', con=engine)
        logging.info("Data from cademycode_courses read successfully.")

        df_jobs = pd.read_sql_query('SELECT * FROM cademycode_student_jobs', con=engine)
        logging.info("Data from cademycode_student_jobs read successfully.")

        df_students = pd.read_sql_query('SELECT * FROM cademycode_students', con=engine)
        logging.info("Data from cademycode_students read successfully.")

        # Convert job_id columns to integers, handling any non-integer values
        logging.info("Converting job_id columns to integers.")
        df_students['job_id'] = pd.to_numeric(df_students['job_id'], errors='coerce').fillna(0).astype('int64')
        df_jobs['job_id'] = pd.to_numeric(df_jobs['job_id'], errors='coerce').fillna(0).astype('int64')

        # Merge the tables into a single DataFrame
        logging.info("Merging tables.")
        df_merged = pd.merge(df_students, df_jobs, how='left', left_on='job_id', right_on='job_id')

        # Ensure the current_career_path_id and career_path_id columns have the same data type
        df_merged['current_career_path_id'] = pd.to_numeric(df_merged['current_career_path_id'], errors='coerce').fillna(0).astype('int64')
        df_courses['career_path_id'] = pd.to_numeric(df_courses['career_path_id'], errors='coerce').fillna(0).astype('int64')

        # Merge the result with courses
        df_final = pd.merge(df_merged, df_courses, how='left', left_on='current_career_path_id', right_on='career_path_id')

        # Validate the final table
        logging.info("Length of DataFrame before merge: %d", len(df_students))
        logging.info("Length of DataFrame after merge: %d", len(df_final))
        print("Length of DataFrame before merge:", len(df_students))
        print("Length of DataFrame after merge:", len(df_final))

        # Check for any missing values after the merge
        missing_values = df_final.isnull().sum()
        logging.info("Missing values in the final DataFrame: %s", missing_values)
        print("Missing values in the final DataFrame:", missing_values)

        # Save the final DataFrame to a new SQLite database
        logging.info("Saving the final DataFrame to a new SQLite database.")
        engine_clean = create_engine('sqlite:///dev/cademycode_clean_local.db')
        df_final.to_sql('cademycode_final_local', con=engine_clean, if_exists='replace', index=False)

        # Save the final DataFrame to a CSV file
        logging.info("Saving the final DataFrame to a CSV file.")
        df_final.to_csv('dev/cademycode_final_local.csv', index=False)

        logging.info("Final CSV and SQLite database created successfully.")
        print("Final CSV and SQLite database created successfully.")

        # Update changelog
        new_rows = len(df_final) - len(df_students)
        update_changelog(new_rows, missing_values.sum())

        # Save the current row count for future comparisons
        save_current_row_count(len(df_final))

    except Exception as e:
        logging.error("Error in data pipeline: %s", e)
        print("Error in data pipeline:", e)
        raise

if __name__ == "__main__":
    main()