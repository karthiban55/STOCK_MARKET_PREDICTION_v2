# run_analysis.py
import sys
from pymongo import MongoClient

# --- 1. SET YOUR CONNECTION STRING ---
# Put your NEW password here
CONNECTION_STRING = "mongodb+srv://KarthibanR:Karthiban@karthicluster.vg1h6b7.mongodb.net/test?retryWrites=true&w=majority"

if "<your_new_password>" in CONNECTION_STRING:
    print("ERROR: Please update the 'CONNECTION_STRING' with your new password.")
    sys.exit(1)

# --- 2. CONNECT TO MONGODB ---
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['stock_project_db'] # Your database
    news_collection = db['news']     # Your news collection
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

# --- 3. DEFINE THE ANALYSIS PIPELINE ---
# This is the "modern" version of MapReduce.
# We want to find the top 10 most active news sources.
pipeline = [
    {
        "$group": {
            "_id": "$source",         # Group all documents by their "source" field
            "article_count": { "$sum": 1 }  # For each document, add 1 to the count
        }
    },
    {
        "$sort": {
            "article_count": -1   # Sort by the count in descending order
        }
    },
    {
        "$limit": 10  # Only show the top 10
    }
]

# --- 4. RUN THE ANALYSIS ---
print("\n--- Running Analysis: Top 10 News Sources ---")
try:
    results = news_collection.aggregate(pipeline)

    for doc in results:
        print(f"  Source: {doc['_id']}, Count: {doc['article_count']}")

except Exception as e:
    print(f"An error occurred: {e}")

client.close()