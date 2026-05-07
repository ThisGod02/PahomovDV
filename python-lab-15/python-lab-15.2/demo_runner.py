from __future__ import annotations

from consumer import OrderStatsConsumer
from producer import OrderEventProducer


def main() -> None:
    producer = OrderEventProducer()
    consumer = OrderStatsConsumer()

    print("Generating mock Kafka events")
    print("----------------------------")
    for order in producer.stream_orders(8):
        print(f"Produced {order['order_id']} for {order['customer']['name']} -> {order['total_amount']}")
        consumer.process(order)

    consumer.print_summary()


if __name__ == "__main__":
    main()
