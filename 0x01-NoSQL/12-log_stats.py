#!/usr/bin/env python3
"""
12-log_stats.py
"""
import pymongo


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    collection = db["nginx"]

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        total_per_method = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {total_per_method}")

    total_status_check = collection.count_documents({
        'method': 'GET',
        'path': '/status'
    })
    print(f"{total_status_check} status check")
