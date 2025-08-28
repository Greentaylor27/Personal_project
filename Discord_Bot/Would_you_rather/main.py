import os
from dotenv import load_dotenv
from supabase import create_client
import Utils.create_starter_csv
from Utils.utils_db import insert_by_row_into_db

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

Utils.create_starter_csv

csv_path = "Data/questions.csv"
table_name = "questions"

rows_inserted = insert_by_row_into_db(supabase, csv_path, table_name)
print(f"✅ {rows_inserted} rows inserted into '{table_name}'")
