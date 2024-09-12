import os
import sqlite3
import json
from collections import Counter
from datetime import datetime, timedelta

# Get the Chrome data path for the current user
chrome_data_path = os.path.join(os.getenv('LOCALAPPDATA'), "Google", "Chrome", "User Data", "Default")
history_db = os.path.join(chrome_data_path, "History")

def fetch_chrome_history(db_path):
    # Connect to the history database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute query to get URL, title, visit count, and visit times from the 'urls' table
        cursor.execute("""
            SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC
        """)
        
        # Fetch all results
        rows = cursor.fetchall()
        
        # Print the history with readable visit times
        print("{:<50} {:<30} {:<10} {}".format("URL", "Title", "Visits", "Last Visit Time"))
        print("="*120)
        
        most_visited = Counter()
        for row in rows:
            url, title, visit_count, last_visit_time = row
            
            # Convert Chrome's timestamp format to human-readable format
            visit_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit_time)
            
            print(f"{url:<50} {title:<30} {visit_count:<10} {visit_time}")
            
            # Add URL to the most visited list
            most_visited[url] += visit_count
        
        # Print most visited sites
        print("\nMost Visited Sites:")
        print("="*120)
        for site, count in most_visited.most_common(10):
            print(f"{site:<50} Visited {count} times")
        
        # Close connection
        cursor.close()
        conn.close()
    
    except sqlite3.OperationalError as e:
        print(f"Error accessing the database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_payment_details():
    # Chrome does not store payment details directly in the SQLite databases; they are often encrypted
    print("\nChrome does not store payment details in a human-readable format.")
    print("For security reasons, payment data is stored securely and requires administrative or browser access.")

# Call the functions to extract history and payment information
print("Extracting Chrome Browsing History...\n")
fetch_chrome_history(history_db)

print("\nExtracting Payment Details...\n")
fetch_payment_details()
