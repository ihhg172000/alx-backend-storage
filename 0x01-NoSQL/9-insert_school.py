#!/usr/bin/env python3
"""
9-insert_school.py
"""


def insert_school(mongo_collection, **kwargs):
    """
    Function that inserts a new document in a collection based on kwargs.
    """
    inserted_document = mongo_collection.insert_one(kwargs)
    return inserted_document.inserted_id
