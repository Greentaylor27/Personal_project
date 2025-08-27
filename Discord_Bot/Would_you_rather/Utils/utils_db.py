import csv
from utils.supabase import init_supabase

def insert_questions_to_db(csv_file):
  supabase = init_supabase()

  with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    rows = [row for row in reader]

    if rows:
      data, count = supabase.table("questions").insert(rows).execute()
      return count
    return 0
