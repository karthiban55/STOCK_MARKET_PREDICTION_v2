from pymongo import MongoClient
from datetime import datetime
import sys

# --- 1. SET YOUR CONNECTION STRING ---
# Replace with your actual connection string from MongoDB Atlas
# Example: "mongodb+srv://your_user:your_password@your_cluster.mongodb.net/..."
CONNECTION_STRING = "mongodb+srv://KarthibanR:Karthiban@karthicluster.vg1h6b7.mongodb.net/"

if "<username>" in CONNECTION_STRING:
    print("="*50)
    print("ERROR: Please update the 'CONNECTION_STRING' variable")
    print("with your actual MongoDB connection string.")
    print("="*50)
    sys.exit(1) # Stop the script

# --- 2. CONNECT TO MONGODB ---
try:
    # Connect to MongoDB
    client = MongoClient(CONNECTION_STRING)
    
    # Ping to confirm connection
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

# Select your database (it will be created if it doesn't exist)
db = client['stock_project_db']


# --- 3. INSERT FAKE TICKERS ---
print("\n--- Populating 'tickers' Collection ---")
try:
    # Get (or create) the 'tickers' collection
    ticker_collection = db['tickers']

    # Your fake ticker data
    fake_tickers = [
      {"symbol": "DUMMY", "name": "Dummy Corp International"},
      {"symbol": "FKSTK", "name": "Fake Stock Industries"},
      {"symbol": "XYZCO", "name": "XYZ Company Ltd."},
      {"symbol": "TEST", "name": "TestCorp Holdings"},
      {"symbol": "NULL", "name": "Nullset Analytics"}
    ]

    # Clear the collection first to avoid duplicates
    deleted_count = ticker_collection.delete_many({}).deleted_count
    print(f"Cleared {deleted_count} old tickers.")

    # Insert the new data
    result = ticker_collection.insert_many(fake_tickers)
    print(f"📈 Inserted {len(result.inserted_ids)} fake tickers.")
    
    # Create an index for fast searching by symbol
    ticker_collection.create_index("symbol", unique=True)
    print("Created index on 'symbol'.")

except Exception as e:
    print(f"Error inserting tickers: {e}")


# --- 4. INSERT FAKE NEWS ---
print("\n--- Populating 'news' Collection ---")
try:
    # Get (or create) the 'news' collection
    news_collection = db['news']

    # Your fake news data (using datetime objects)
    fake_news = [
      {
        "headline": "Market Hits All-Time High on Tech Speculation",
        "source": "Demo News Network",
        "timestamp": datetime.fromisoformat("2025-10-31T10:30:00Z"),
        "summary": "Analysts are stunned as the market, led by the tech sector, reached a new peak."
      },
      {
        "headline": "Dummy Corp (DUMMY) Announces 'Revolutionary' New Product",
        "source": "Fake Financial Times",
        "timestamp": datetime.fromisoformat("2025-10-31T09:15:00Z"),
        "summary": "Shares for Dummy Corp surged 15% in pre-market trading."
      },
      {
        "headline": "Economic Outlook: Stable with Cautious Optimism",
        "source": "Project Data Times",
        "timestamp": datetime.fromisoformat("2025-10-30T17:45:00Z"),
        "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
      }
    ]

    # Clear the collection first
    deleted_count = news_collection.delete_many({}).deleted_count
    print(f"Cleared {deleted_count} old news articles.")

    # Insert the new data
    result = news_collection.insert_many(fake_news)
    print(f"📰 Inserted {len(result.inserted_ids)} fake news articles.")

    # Create an index to quickly find the newest articles
    news_collection.create_index([("timestamp", -1)])
    print("Created descending index on 'timestamp'.")

except Exception as e:
    print(f"Error inserting news: {e}")


# --- 5. FINISH ---
print("\n✅ Database population complete.")
client.close()
print("Connection to MongoDB closed.")