#!/usr/bin/env python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """lists documents"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
