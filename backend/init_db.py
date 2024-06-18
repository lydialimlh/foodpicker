import duckdb
import os

folder_path = os.getcwd()

file_path = folder_path + "/backend/food_choices.csv"

duckdb.execute(f"CREATE OR REPLACE TABLE food AS SELECT * FROM '{file_path}';")

query_all = duckdb.execute("SELECT * FROM food;")

print(
    "Database successfully initiated. Current records available: \n",
    query_all.fetchdf(),
)
