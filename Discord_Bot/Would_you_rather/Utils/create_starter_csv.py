import uuid

numbers = "0123456789"

with open("Data/question.txt", "r") as file:
  lines = file.readlines()

with open("Data/questions.csv", "w") as f:
  f.write("id,question\n") #header

  for line in lines:
    id = uuid.uuid4()
    parts = line.split(". ", 1)

    if len(parts) < 2:
      continue
    
    question = parts[1].strip()
    question = ''.join(c for c in question if c not in numbers) # remove numbers if needed
    question = question.replace('"', '""')
    question = f'"{question}"'

    f.write(f"{id},{question}\n")

print("CSV file created successfully.")
