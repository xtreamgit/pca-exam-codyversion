import json
from pymongo import MongoClient
import os

def load_questions_to_db():
    # Check if data.json exists in the root directory
    if not os.path.exists('data.json'):
        print("The data.json file was not found in the root of the project directory. Make sure the data.json is in the root of the project")
        return
    printf("Trying to connect to MongoDB")
    # Connect to MongoDB - local connection    
    client = MongoClient('mongodb://localhost:27017/')
    
    # Connect to MongoDB - container connection 
    # client = MongoClient('mongodb://mongo:27017/examDB')
    db = client.examDB
    questions_collection = db.questions

    # Ensure the collection is empty before loading new data
    # Hector's note: I commented this out because the delete_many statement is not required for now.
    # questions_collection.delete_many({})

    # Load data from JSON file
    with open('data.json', 'r') as file:
        questions_data = json.load(file)

    # Insert data into MongoDB
    questions_collection.insert_many(questions_data)

    print("Data loaded successfully into MongoDB.")

if __name__ == "__main__":
    load_questions_to_db()



