from __future__ import annotations

import argparse
import json
from collections import defaultdict

from kafka import KafkaConsumer


class OrderStatsConsumer:
    def __init__(self):
        self.stats = {
            "orders_processed": 0,
            "revenue_total": 0,
            "by_category": defaultdict(float),
            "by_city": defaultdict(int),
        }

    def process(self, order: dict) -> None:
        self.stats["orders_processed"] += 1
        self.stats["revenue_total"] += order["total_amount"]
        self.stats["by_city"][order["customer"]["city"]] += 1
        for item in order["items"]:
            self.stats["by_category"][item["category"]] += item["total_price"]

    def print_summary(self) -> None:
        print("\nLive order statistics")
        print("---------------------")
        print(f"Orders processed: {self.stats['orders_processed']}")
        print(f"Revenue total: {self.stats['revenue_total']}")
        print(f"By city: {dict(self.stats['by_city'])}")
        print(f"By category: {dict(self.stats['by_category'])}")

    def consume_kafka(self, bootstrap_servers: str, topic: str, max_messages: int) -> None:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="lab15-consumer-group",
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        )
        try:
            for index, message in enumerate(consumer, start=1):
                self.process(message.value)
                if index >= max_messages:
                    break
        finally:
            consumer.close()
        self.print_summary()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["kafka"], default="kafka")
    parser.add_argument("--max-messages", type=int, default=10)
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--topic", default="orders")
    args = parser.parse_args()

    consumer = OrderStatsConsumer()
    consumer.consume_kafka(args.bootstrap_servers, args.topic, args.max_messages)


if __name__ == "__main__":
    main()
