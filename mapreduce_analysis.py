import sys
from pymongo import MongoClient

# --- 1. SET YOUR CONNECTION STRING ---
# Put your NEW password here
CONNECTION_STRING = "mongodb+srv://KarthibanR:Karthibann@karthicluster.vg1h6b7.mongodb.net/test?retryWrites=true&w=majority"

if "<karthiban2006>" in CONNECTION_STRING:
    print("="*50)
    print("ERROR: Please update the 'CONNECTION_STRING' with your new password.")
    print("="*50)
    sys.exit(1)

# --- 2. CONNECT TO MONGODB ---
try:
    client = MongoClient(CONNECTION_STRING)
    db = client['stock_project_db'] # Your database
    news_collection = db['news']
    tickers_collection = db['tickers']
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)


# --- ANALYSIS FUNCTIONS (Using the correct 'aggregate' method) ---

def analysis_1_top_news_sources():
    """Finds the top 10 most active news sources."""
    print("\n--- Analysis 1: Top 10 News Sources ---")
    pipeline = [
        {
            "$group": {
                "_id": "$source",
                "article_count": { "$sum": 1 }
            }
        },
        { "$sort": { "article_count": -1 } },
        { "$limit": 10 }
    ]
    results = news_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Source: {doc['_id']}, Count: {doc['article_count']}")

def analysis_2_keyword_in_headlines():
    """Finds how many headlines contain the word 'Market'."""
    print("\n--- Analysis 2: Keyword 'Market' Count ---")
    pipeline = [
        {
            "$match": {
                "headline": { "$regex": "Market", "$options": "i" }
            }
        },
        {
            "$count": "total_market_mentions"
        }
    ]
    results = news_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Found: {doc}")

def analysis_3_count_articles_by_year():
    """Counts how many articles were published per year."""
    print("\n--- Analysis 3: Article Count by Year ---")
    pipeline = [
        {
            "$group": {
                "_id": { "$year": "$timestamp" },
                "article_count": { "$sum": 1 }
            }
        },
        { "$sort": { "_id": 1 } }
    ]
    results = news_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Year: {doc['_id']}, Count: {doc['article_count']}")


def analysis_7_find_news_about_fake_tickers():
    """Finds news articles that mention a fake ticker symbol."""
    print("\n--- Analysis 7: News Mentioning Fake Tickers ---")
    pipeline = [
        {
            "$lookup": {
                "from": "news",
                "localField": "symbol",
                "foreignField": "headline",
                "as": "related_articles"
            }
        },
        {
            "$match": {
                "related_articles": { "$ne": [] }
            }
        },
        {
            "$project": {
                "_id": 0,
                "symbol": "$symbol",
                "headlines": "$related_articles.headline"
            }
        }
    ]
    results = tickers_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Ticker: {doc['symbol']}")
        for headline in doc['headlines']:
            print(f"    - {headline}")

def analysis_8_busiest_day_of_week():
    """Finds which day of the week has the most news, on average."""
    print("\n--- Analysis 8: Busiest Day of the Week ---")
    pipeline = [
        {
          "$group": {
            "_id": {
              "dayOfWeek": { "$dayOfWeek": "$timestamp" }
            },
            "articles_on_this_day": { "$sum": 1 }
          }
        },
        {
          "$group": {
            "_id": "$_id.dayOfWeek",
            "average_articles": { "$avg": "$articles_on_this_day" }
          }
        },
        {
          "$project": {
            "_id": 0,
            "day": {
              "$switch": {
                "branches": [
                  { "case": { "$eq": [ "$_id", 1 ] }, "then": "Sunday" },
                  { "case": { "$eq": [ "$_id", 2 ] }, "then": "Monday" },
                  { "case": { "$eq": [ "$_id", 3 ] }, "then": "Tuesday" },
                  { "case": { "$eq": [ "$_id", 4 ] }, "then": "Wednesday" },
                  { "case": { "$eq": [ "$_id", 5 ] }, "then": "Thursday" },
                  { "case": { "$eq": [ "$_id", 6 ] }, "then": "Friday" },
                  { "case": { "$eq": [ "$_id", 7 ] }, "then": "Saturday" }
                ],
                "default": "Unknown"
              }
            },
            "average_articles": { "$round": [ "$average_articles", 2 ] }
          }
        },
        { "$sort": { "average_articles": -1 } }
    ]
    results = news_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Day: {doc['day']}, Average: {doc['average_articles']}")

def analysis_9_sources_mentioning_tickers():
    """Finds which news sources mention tickers most often."""
    print("\n--- Analysis 9: Sources That Mention Tickers ---")
    pipeline = [
        {
          "$lookup": {
            "from": "news",
            "let": { "ticker_symbol": "$symbol" },
            "pipeline": [
              {
                "$match": {
                  "$expr": {
                    "$regexMatch": {
                      "input": "$headline",
                      "regex": "$$ticker_symbol"
                    }
                  }
                }
              }
            ],
            "as": "related_articles"
          }
        },
        { "$unwind": "$related_articles" },
        {
          "$group": {
            "_id": "$related_articles.source",
            "total_mentions": { "$sum": 1 }
          }
        },
        { "$sort": { "total_mentions": -1 } },
        { "$limit": 5 }
    ]
    results = tickers_collection.aggregate(pipeline)
    for doc in results:
        print(f"  Source: {doc['_id']}, Mentions: {doc['total_mentions']}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        analysis_1_top_news_sources()
        analysis_2_keyword_in_headlines()
        analysis_3_count_articles_by_year()
        analysis_7_find_news_about_fake_tickers()
        analysis_8_busiest_day_of_week()
        analysis_9_sources_mentioning_tickers()

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
    finally:
        client.close()
        print("\n✅ Analysis complete. Connection to MongoDB closed.")