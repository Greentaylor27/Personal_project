import uuid

numbers = "0123456789"

with open("Data/question.txt", "r") as file:
  lines = file.readlines()

with open("Data/questions.csv", "w") as f:
  f.write("id,option_a,option_b\n") #header

  for line in lines:
    qid = uuid.uuid4()
    parts = line.split(". ", 1)

    if len(parts) < 2:
      continue
    
    question = parts[1].strip()
    question = ''.join(c for c in question if c not in numbers) # remove numbers if needed
    
    # Splitting at OR
    if " OR " not in question:
      continue
    option_a, option_b = map(str.strip, question.split(" OR ", 1))
    
    option_a = option_a.replace('"', '""')
    option_b = option_b.replace('"', '""')

    f.write(f"{qid},{option_a},{option_b}\n")

print("CSV file created successfully.")
