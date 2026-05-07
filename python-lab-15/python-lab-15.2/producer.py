from __future__ import annotations

import argparse
import json
import random
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from kafka import KafkaProducer


PRODUCTS = [
    {"product_id": 1, "name": "Laptop", "price": 75000, "category": "Electronics"},
    {"product_id": 2, "name": "Mouse", "price": 1500, "category": "Electronics"},
    {"product_id": 3, "name": "SQL Book", "price": 2500, "category": "Books"},
    {"product_id": 4, "name": "Keyboard", "price": 5000, "category": "Electronics"},
    {"product_id": 5, "name": "Monitor", "price": 25000, "category": "Electronics"},
    {"product_id": 6, "name": "Python Book", "price": 3500, "category": "Books"},
]

CUSTOMERS = [
    {"id": 1, "name": "Anna Smirnova", "city": "Moscow"},
    {"id": 2, "name": "Peter Ivanov", "city": "Saint Petersburg"},
    {"id": 3, "name": "Maria Sidorova", "city": "Kazan"},
    {"id": 4, "name": "Ivan Petrov", "city": "Moscow"},
    {"id": 5, "name": "Elena Kozlova", "city": "Novosibirsk"},
]


@dataclass
class OrderEventProducer:
    bootstrap_servers: str = "localhost:9092"
    topic: str = "orders"

    def generate_order(self) -> dict:
        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)
        quantity = random.randint(1, 3)
        return {
            "order_id": str(uuid.uuid4())[:8],
            "timestamp": datetime.utcnow().isoformat(),
            "customer": customer,
            "items": [
                {
                    "product_id": product["product_id"],
                    "product_name": product["name"],
                    "category": product["category"],
                    "quantity": quantity,
                    "unit_price": product["price"],
                    "total_price": quantity * product["price"],
                }
            ],
            "total_amount": quantity * product["price"],
            "payment_method": random.choice(["card", "cash", "online"]),
        }

    def stream_orders(self, count: int) -> Iterable[dict]:
        for _ in range(count):
            yield self.generate_order()

    def send_to_kafka(self, count: int, interval_seconds: float) -> None:
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            key_serializer=lambda key: str(key).encode("utf-8"),
        )
        try:
            for order in self.stream_orders(count):
                producer.send(self.topic, key=order["customer"]["id"], value=order).get(timeout=10)
                print(f"Sent order {order['order_id']} with total {order['total_amount']}")
                time.sleep(interval_seconds)
        finally:
            producer.flush()
            producer.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "kafka"], default="mock")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--interval", type=float, default=0.2)
    args = parser.parse_args()

    producer = OrderEventProducer()
    if args.mode == "kafka":
        producer.send_to_kafka(args.count, args.interval)
    else:
        for order in producer.stream_orders(args.count):
            print(json.dumps(order, ensure_ascii=False))


if __name__ == "__main__":
    main()
