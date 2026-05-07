from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


load_dotenv()


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_demo_outputs(base_dir: Path) -> dict[str, pd.DataFrame]:
    customers = load_csv(base_dir / "seed" / "customers.csv")
    products = load_csv(base_dir / "seed" / "products.csv")
    orders = load_csv(base_dir / "seed" / "orders.csv")
    order_items = load_csv(base_dir / "seed" / "order_items.csv")

    merged = order_items.merge(products, on="product_id", how="left")
    merged["price_at_order_time"] = merged["price"]
    merged["line_total"] = merged["quantity"] * merged["price_at_order_time"]

    order_totals = merged.groupby("order_id", as_index=False).agg(
        order_total=("line_total", "sum"),
        item_count=("quantity", "sum"),
    )
    orders_enriched = orders.merge(order_totals, on="order_id", how="left")

    delivered = orders_enriched[orders_enriched["status"] == "Delivered"]
    customer_totals = delivered.groupby("customer_id", as_index=False).agg(
        purchase_total=("order_total", "sum")
    )
    customers_enriched = customers.merge(customer_totals, on="customer_id", how="left").fillna(
        {"purchase_total": 0}
    )

    return {
        "customers_enriched": customers_enriched,
        "products": products,
        "orders_enriched": orders_enriched,
        "order_items_enriched": merged,
    }


def export_outputs(base_dir: Path, outputs: dict[str, pd.DataFrame]) -> None:
    exports_dir = base_dir / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    for name, frame in outputs.items():
        frame.to_csv(exports_dir / f"{name}.csv", index=False)

    schema_path = base_dir / "schema" / "base_schema.json"
    export_schema_path = exports_dir / "base_schema_export.json"
    export_schema_path.write_text(schema_path.read_text(encoding="utf-8"), encoding="utf-8")

    views_summary = {
        "all_orders": outputs["orders_enriched"].sort_values("order_date", ascending=False).to_dict("records"),
        "active_orders": outputs["orders_enriched"][
            ~outputs["orders_enriched"]["status"].isin(["Delivered", "Cancelled"])
        ].to_dict("records"),
    }
    (exports_dir / "views_summary.json").write_text(
        json.dumps(views_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline-demo", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    outputs = build_demo_outputs(base_dir)
    export_outputs(base_dir, outputs)

    if args.offline_demo:
        print("Offline Airtable demo completed")
        print(outputs["orders_enriched"].to_string(index=False))
        print(f"Artifacts: {base_dir / 'exports'}")
        return

    token = os.getenv("AIRTABLE_TOKEN")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    if token and base_id:
        print("Credentials detected. CSV and schema pack is ready for Airtable import/API sync.")
    else:
        print("No Airtable credentials found. Offline export pack has been generated.")


if __name__ == "__main__":
    main()
