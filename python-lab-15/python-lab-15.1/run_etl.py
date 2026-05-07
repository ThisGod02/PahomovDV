from __future__ import annotations

from pathlib import Path

from etl_pipeline import SalesETLPipeline


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    pipeline = SalesETLPipeline(
        csv_path=base_dir / "data" / "sales.csv",
        db_path=base_dir / "sales.db",
        reports_dir=base_dir / "reports",
    )
    result = pipeline.run()

    print("\nAggregated data")
    print("---------------")
    print(result["aggregated"].to_string(index=False))
    print(f"\nSQLite DB: {base_dir / 'sales.db'}")
    print(f"Charts: {base_dir / 'reports'}")


if __name__ == "__main__":
    main()
