import uuid


number = str(range(0, 9)) # used later to remove numbers from questions


file = open("question.txt", "r") # opens a text file with questions in it

lines = file.readlines() # reads each line of the text file


for line in lines: # loops through each line
      
      with open("questions.csv", "a+") as f: # opens/creates a csv file to use to upload questions to the database

          f.write("id, question\n") # writes the header row to the csv file

          id = uuid.uuid4() # creates a unique id for each question

          parts = line.split(". ", 1) # splits the line at the first instance of ". " to remove numbers from the question

          if len(parts) < 2: # checks if the split was successful
               continue # skips to the next iteration if the split was not successful
          
          question = parts[1] # takes the second part of the split (the question itself)

          question = question.strip() # removes any leading/trailing whitespace characters

          question = question.replace('"', '""') # escapes any double quotes in the question for csv format

          question = f'"{question}"' # wraps the question in double quotes for csv format

          f.write(f"{id}, {question}\n")
          f.close()
file.close()
print("CSV file created successfully.")
