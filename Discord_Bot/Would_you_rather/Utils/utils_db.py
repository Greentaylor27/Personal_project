from supabase import Client
import random
import csv
import uuid

def check_if_table_exists(supabase: Client, table_name: str) -> bool:
    """Check if a table exists in the Supabase database."""
    try:
        result = (
            supabase.postgrest
            .from_("information_schema.tables")
            .select("table_name")
            .eq("table_name", table_name)
            .execute()
        )
        return len(result.data) > 0
    except Exception as e:
        return False


def load_csv_without_header(csv_path: str) -> list[dict]:
  """
    Loads csv and returns a list of dict skipping the header automatically

  Args:
      csv_path (str): Path to the CSV

  Returns:
      list[dict]: Basically the csv without the header
  """
  rows = []
  with open(csv_path, "r") as f:
      reader = csv.DictReader(f)
      for row in reader:
          rows.append(row)
  return rows

def insert_by_row_into_db(supabase: Client, csv_path: str, table_name: str) -> int:
  """
    Reads a CSV file and inserts rows into a specified Supabase table

  Args:
      supabase (Client): Supabase Client
      csv_path (str): Path to CSV
      table_name (str): Table name

  Returns:
      int: 0 for success
  """
  rows_inserted = 0
  try:
     rows = load_csv_without_header(csv_path)

     for row in rows:
        data = {
           "id": str(uuid.uuid4()),
           "option_a": row["option_a"].strip(),
           "option_b": row["option_b"].strip(),
           }
        response = supabase.table(table_name).insert(data).execute()

        if response.data:
           rows_inserted += 1
        else:
           print("Insert failed:", response)

     print(f"✅ {rows_inserted} rows inserted into '{table_name}'")
     return rows_inserted

  except Exception as e:
     print("Error inserting rows:", e)
     return rows_inserted

def get_random_question(supabase: Client, table_name: str) -> dict | None:
    """
    Fetch a random question from the Supabase table.

    Args:
        supabase (Client): Supabase client instance.
        table_name (str): Name of the table

    Returns:
        dict | None: a random question with option_a and option_b, or None
    """
    try:
       # Pull all rows
       response = supabase.table(table_name).select("*").execute()
       rows = response.data

       if not rows:
          return None
       
       # Pick a random row
       question = random.choice(rows)
       return question
    
    except Exception as e:
       print("Error fetching question:", e)
       return None
