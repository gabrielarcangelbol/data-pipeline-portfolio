---
### README.md

# Data Pipeline Update Process

## Overview
For this project, you’ll build a data engineering pipeline to regularly transform a messy database into a clean source of truth for an analytics team.

### Scenario
You’ll be working with a mock database of long-term cancelled subscribers for a fictional subscription company. This database is regularly updated from multiple sources and needs to be routinely cleaned and transformed into usable shape with as little human intervention as possible.

### About the Data
It’s important to practice working with customer data, especially as a data engineer. But it would be unethical to share actual customer data, so we’ve developed a realistic but entirely fictional dataset for you to use. Because we’re an online education company, our version of the dataset is based around a fictional education company called Cademycode.

Feel free to come up with your own company/product for your project, and modify our database to match your company’s story! There are a few services to help you generate mock data, including generatedata.com and Mockaroo.

### Project Objectives
- Complete a project to add to your portfolio.
- Use Jupyter notebooks to explore and clean a dataset.
- Use Python to automate data cleaning and transformation using unit tests and error logging.
- Use Bash scripts to automate file management and run scripts.

### Prerequisites
- Intermediate and Advanced Python 3
- Pandas
- Bash Scripting

Instead of a step-by-step tutorial, this project contains a series of open-ended requirements which describe the project you’ll be building. There are many possible ways to correctly fulfill all of these requirements. You should expect to use the internet, Codecademy, and other resources when you encounter a problem that you cannot easily solve.

## Folder Structure
The project directory is organized as follows:

```
project-root/
│
├── dev/
│   ├── cademycode_clean_local.db
│   ├── cademycode_final_local.csv
│   ├── changelog.txt
│   ├── data_pipeline.log
│   └── previous_row_count.txt
│
├── prod/
│   ├── cademycode_clean_local.db
│   ├── cademycode_final_local.csv
│
├── data_pipeline.py
├── test_data_pipeline.py
└── run_pipeline.sh
```

### Description of Files
- **dev/**: Development directory where temporary files and logs are generated and stored.
  - `cademycode_clean_local.db`: SQLite database generated after processing the data.
  - `cademycode_final_local.csv`: CSV file generated after processing the data.
  - `changelog.txt`: Changelog file that records the details of each update.
  - `data_pipeline.log`: Log file that records the details of the script execution.
  - `previous_row_count.txt`: File that stores the row count of the previous version of the table.

- **prod/**: Production directory where the generated files are moved after a successful update.
  - `cademycode_clean_local.db`: SQLite database generated after processing the data.
  - `cademycode_final_local.csv`: CSV file generated after processing the data.

- **data_pipeline.py**: Main Python script that processes the data and generates the files.
- **test_data_pipeline.py**: Unit test script to verify that the data pipeline works correctly.
- **run_pipeline.sh**: Bash script that runs the main Python script, verifies the generated files, runs the unit tests, checks the logs, and moves the files to production if an update is detected.

## Instructions for Running the Update Process

1. **Activate the Virtual Environment**: Make sure to activate your virtual environment before running the Bash script.

```bash
source "/DataEngineer_Codecademy/.venv/Scripts/activate"
```

2. **Run the Bash Script**: Run the Bash script to process the data and move the generated files to production.

```bash
bash run_pipeline.sh
```

## Changelog and Version Control System

- **Changelog**: The `dev/changelog.txt` file records the details of each update, including the number of new rows added and the amount of missing data. The Bash script checks this file to detect updates and move the files to production if a new version is detected. Example changelog content:

```plaintext
## [2025-02-26 16:23:09]
### Added
- New rows added: 2006
- Missing data counts: 2981
### Fixed
- Fixed missing table errors for `cademycode_courses`
### Changed
- Combined tables into `cademycode_final_local`

Version 1.0.1
- New rows added: 100
- Missing data counts: 0

## [2025-02-26 16:25:51]
### Added
- New rows added: 2006
- Missing data counts: 2981
### Fixed
- Fixed missing table errors for `cademycode_courses`
### Changed
- Combined tables into `cademycode_final_local`

## [2025-02-26 16:28:16]
### Added
- New rows added: 2301
- Missing data counts: 3075
### Fixed
- Fixed missing table errors for `cademycode_courses`
### Changed
- Combined tables into `cademycode_final_local`

## [2025-02-26 16:28:50]
### Added
- New rows added: 2301
- Missing data counts: 3075
### Fixed
- Fixed missing table errors for `cademycode_courses`
### Changed
- Combined tables into `cademycode_final_local`

## [2025-02-26 16:31:47]
### Added
- New rows added: 2301
- Missing data counts: 3075
### Fixed
- Fixed missing table errors for `cademycode_courses`
### Changed
- Combined tables into `cademycode_final_local`
```

- **Error Logs**: The `dev/data_pipeline.log` file records the details of the script execution, including any errors that occur during the process. You can review this file for more information about any issues that occur. Example log content:

```plaintext
2025-02-26 16:23:09,279:INFO:Reading data from the database.
2025-02-26 16:23:09,281:INFO:Data from cademycode_courses read successfully.
2025-02-26 16:23:09,282:INFO:Data from cademycode_student_jobs read successfully.
2025-02-26 16:23:09,300:INFO:Data from cademycode_students read successfully.
2025-02-26 16:23:09,300:INFO:Converting job_id columns to integers.
2025-02-26 16:23:09,304:INFO:Merging tables.
2025-02-26 16:23:09,313:INFO:Length of DataFrame before merge: 5000
2025-02-26 16:23:09,314:INFO:Length of DataFrame after merge: 7006
2025-02-26 16:23:09,317:INFO:Missing values in the final DataFrame: uuid                        0
name                        0
dob                         0
sex                         0
contact_info                0
job_id                      0
num_course_taken          353
current_career_path_id      0
time_spent_hrs            657
job_category                0
avg_salary                  0
career_path_id            657
career_path_name          657
hours_to_complete         657
dtype: int64
2025-02-26 16:23:09,319:INFO:Saving the final DataFrame to a new SQLite database.
2025-02-26 16:23:09,416:INFO:Saving the final DataFrame to a CSV file.
2025-02-26 16:23:09,475:INFO:Final CSV and SQLite database created successfully.
```

- **Previous Row Count**: The `dev/previous_row_count.txt` file stores the row count of the previous version of the table for comparison with the current count. Example file content:

```plaintext
8301
```

## Necessary Files
Download our starter kit for the project. When you unzip this kit, you should find a folder named `/dev` containing two databases:

- `cademycode.db`
- `cademycode_updated.db`

Use the first database to explore the data and develop your project code. Once your code is complete, use the updated database to test your update process.

## Going Off Platform
For this particular project, you will be using Jupyter Notebooks, bash scripting, and Python. If you need help with your setup, read our articles about getting started off platform:

- Command Line Interface Setup
- Setting up Python and Jupyter with Anaconda
- Getting Started with Jupyter

By following these steps and using the provided resources, you should be able to successfully run the code and understand the project structure and analysis.

---
