import unittest
import pandas as pd
from sqlalchemy import create_engine

class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        # Establish the database connection to SQLite
        self.engine = create_engine('sqlite:///dev/cademycode_clean_local.db')

    def test_schema(self):
        # Check that the updated database has the expected final table
        updated_tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con=self.engine)
        self.assertIn('cademycode_final_local', updated_tables['name'].tolist())

    def test_table_joins(self):
        # Check if the tables will join properly
        # This test is no longer applicable since the final database only contains the combined table
        pass

    def test_new_data(self):
        # Check if there is any new data
        df_final = pd.read_sql_query('SELECT * FROM cademycode_final_local', con=self.engine)
        previous_row_count = self.get_previous_row_count()
        current_row_count = len(df_final)
        
        # Check if the number of rows has increased
        if current_row_count > previous_row_count:
            print("The number of rows has increased.")
        # Check if the number of rows has remained the same
        elif current_row_count == previous_row_count:
            print("The number of rows has remained the same.")
        
        # Ensure that the current number of rows is greater than or equal to the previous number of rows
        self.assertGreaterEqual(current_row_count, previous_row_count)

    def get_previous_row_count(self):
        # This function should return the row count from the previous version of the table
        # For this example, we'll assume it's stored in a file called 'previous_row_count.txt'
        try:
            with open('dev/previous_row_count.txt', 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            # If the file doesn't exist, assume there were no previous rows
            return 0

    def save_current_row_count(self, row_count):
        # Save the current row count to a file for future comparisons
        with open('dev/previous_row_count.txt', 'w') as file:
            file.write(str(row_count))

if __name__ == '__main__':
    unittest.main()