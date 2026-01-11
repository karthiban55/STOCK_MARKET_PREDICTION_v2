import sys
import random
from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta

# --- 1. SET YOUR CONNECTION STRING ---
# Put your NEW password here.
# I am using the cluster name you provided.
CONNECTION_STRING = "mongodb+srv://KarthibanR:Karthiban@karthicluster.vg1h6b7.mongodb.net/test?retryWrites=true&w=majority"

if "<your_new_password>" in CONNECTION_STRING:
    print("="*50)
    print("ERROR: Please update the 'CONNECTION_STRING' variable")
    print("with your new password.")
    print("="*50)
    sys.exit(1) # Stop the script

# --- 2. CONNECT TO MONGODB ---
try:
    client = MongoClient(CONNECTION_STRING)
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

# Select your database
db = client['stock_project_db']

# --- 3. SETUP FAKER ---
fake = Faker()

# --- 4. DATA GENERATION ---
NUM_TICKERS = 5000
NUM_NEWS = 45000

# Helper function to insert in batches
def batch_insert(collection, data_list, batch_size=1000):
    total = len(data_list)
    for i in range(0, total, batch_size):
        batch = data_list[i:i + batch_size]
        collection.insert_many(batch)
        print(f"Inserted batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size} into '{collection.name}'...")
    print(f"✅ Finished inserting {total} records into '{collection.name}'.")

# --- Generate Tickers ---
print(f"\n--- Generating {NUM_TICKERS} Tickers ---")
ticker_collection = db['tickers']
tickers_to_insert = []
ticker_symbols = set() # Use a set to avoid duplicate symbols

while len(ticker_symbols) < NUM_TICKERS:
    # Generate a 3 to 5 letter symbol
    length = random.randint(3, 5)
    symbol = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
    ticker_symbols.add(symbol)

for symbol in ticker_symbols:
    tickers_to_insert.append({
        "symbol": symbol,
        "name": fake.company()
    })

# Clear old data and insert new data
ticker_collection.delete_many({})
print(f"Cleared 'tickers' collection.")
batch_insert(ticker_collection, tickers_to_insert)

# --- Generate News ---
print(f"\n--- Generating {NUM_NEWS} News Articles ---")
news_collection = db['news']
news_to_insert = []
ticker_list = list(ticker_symbols) # Convert set to list for random.choice

sources = [fake.company() + " News" for _ in range(50)] # 50 random sources
headlines_templates = [
    "Market Hits All-Time High on {sector} Speculation",
    "{ticker} Stock Surges After Positive Earnings Report",
    "Economic Outlook: {adjective} with Cautious Optimism",
    "{ticker} Announces 'Revolutionary' New Product",
    "Analysts Downgrade {ticker} to 'Sell'",
    "{sector} Sector Sees Unprecedented Growth"
]

for _ in range(NUM_NEWS):
    template = random.choice(headlines_templates)
    headline = template.format(
        ticker=random.choice(ticker_list),
        sector=random.choice(["Tech", "Finance", "Healthcare", "Retail"]),
        adjective=random.choice(["Stable", "Volatile", "Strong"])
    )
    
    news_to_insert.append({
        "headline": headline,
        "source": random.choice(sources),
        "timestamp": fake.date_time_between(start_date='-2y', end_date='now'),
        "summary": fake.paragraph(nb_sentences=3)
    })

# Clear old data and insert new data
news_collection.delete_many({})
print(f"Cleared 'news' collection.")
batch_insert(news_collection, news_to_insert)

# --- 5. FINISH ---
print("\n🎉 All 50,000 fake records have been inserted.")
client.close()
print("Connection to MongoDB closed.")