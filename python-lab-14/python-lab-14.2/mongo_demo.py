from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import mongomock
from pymongo import MongoClient


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_database():
    mongo_uri = os.getenv("MONGODB_URI")
    if mongo_uri:
        client = MongoClient(mongo_uri)
    else:
        client = mongomock.MongoClient()
    return client["shop_mongo"]


def seed(db) -> None:
    db.users.delete_many({})
    db.products.delete_many({})
    db.orders.delete_many({})

    db.users.insert_many(
        [
            {
                "_id": 1,
                "email": "alice@example.com",
                "full_name": "Alice Smith",
                "created_at": utc_now(),
                "address": {"city": "Moscow", "street": "Tverskaya", "zipcode": "101000"},
            },
            {
                "_id": 2,
                "email": "bob@example.com",
                "full_name": "Bob Johnson",
                "created_at": utc_now(),
                "address": {"city": "Saint Petersburg", "street": "Nevsky", "zipcode": "191186"},
            },
            {
                "_id": 3,
                "email": "carol@example.com",
                "full_name": "Carol Miller",
                "created_at": utc_now(),
                "address": {"city": "Kazan", "street": "Baumana", "zipcode": "420111"},
            },
        ]
    )

    db.products.insert_many(
        [
            {"_id": 1, "name": "Laptop", "category": "Electronics", "price": 75000, "stock_quantity": 10},
            {"_id": 2, "name": "Mouse", "category": "Electronics", "price": 1500, "stock_quantity": 50},
            {"_id": 3, "name": "SQL Book", "category": "Books", "price": 2500, "stock_quantity": 30},
            {"_id": 4, "name": "Keyboard", "category": "Electronics", "price": 5000, "stock_quantity": 15},
            {"_id": 5, "name": "Python Book", "category": "Books", "price": 3500, "stock_quantity": 20},
        ]
    )

    db.orders.insert_many(
        [
            {
                "_id": 1,
                "user_id": 1,
                "order_date": datetime(2024, 2, 1, 10, 0, 0),
                "status": "completed",
                "items": [
                    {"product_id": 1, "quantity": 1, "price": 75000},
                    {"product_id": 2, "quantity": 2, "price": 1500},
                ],
            },
            {
                "_id": 2,
                "user_id": 2,
                "order_date": datetime(2024, 2, 2, 11, 30, 0),
                "status": "completed",
                "items": [
                    {"product_id": 3, "quantity": 1, "price": 2500},
                    {"product_id": 4, "quantity": 1, "price": 5000},
                ],
            },
            {
                "_id": 3,
                "user_id": 3,
                "order_date": utc_now() - timedelta(days=45),
                "status": "cancelled",
                "items": [{"product_id": 5, "quantity": 1, "price": 3500}],
            },
        ]
    )


def sanitize(document: Any) -> Any:
    if isinstance(document, dict):
        return {key: sanitize(value) for key, value in document.items()}
    if isinstance(document, list):
        return [sanitize(item) for item in document]
    if isinstance(document, datetime):
        return document.isoformat()
    return document


def print_block(title: str, data: Any) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    print(json.dumps(sanitize(data), indent=2, ensure_ascii=False))


def read_alice_orders(db):
    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info",
            }
        },
        {"$unwind": "$user_info"},
        {"$match": {"user_info.email": "alice@example.com"}},
        {
            "$addFields": {
                "total_amount": {
                    "$sum": {
                        "$map": {
                            "input": "$items",
                            "as": "item",
                            "in": {"$multiply": ["$$item.quantity", "$$item.price"]},
                        }
                    }
                }
            }
        },
    ]
    documents = list(db.orders.aggregate(pipeline))
    for document in documents:
        document["total_amount"] = sum(
            item["quantity"] * item["price"]
            for item in document.get("items", [])
        )
    return documents


def add_discount_for_expensive_orders(db):
    for order in db.orders.find():
        total_amount = sum(item["quantity"] * item["price"] for item in order["items"])
        if total_amount > 80000:
            db.orders.update_one({"_id": order["_id"]}, {"$set": {"discount": 10}})


def delete_old_cancelled_orders(db):
    cutoff = utc_now() - timedelta(days=30)
    db.orders.delete_many({"status": "cancelled", "order_date": {"$lt": cutoff}})


def aggregate_by_category(db):
    pipeline = [
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product",
            }
        },
        {"$unwind": "$product"},
        {
            "$group": {
                "_id": "$product.category",
                "total_sold": {"$sum": "$items.quantity"},
                "total_revenue": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}},
            }
        },
        {"$sort": {"total_revenue": -1}},
    ]
    return list(db.orders.aggregate(pipeline))


def main() -> None:
    db = get_database()
    seed(db)
    print_block("Alice orders", read_alice_orders(db))
    add_discount_for_expensive_orders(db)
    delete_old_cancelled_orders(db)
    print_block("Orders after update/delete", list(db.orders.find({}, {"_id": 1, "status": 1, "discount": 1})))
    print_block("Revenue by category", aggregate_by_category(db))


if __name__ == "__main__":
    main()
