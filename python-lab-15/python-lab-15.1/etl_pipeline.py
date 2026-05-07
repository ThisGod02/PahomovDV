from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine


matplotlib.use("Agg")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SalesETLPipeline:
    def __init__(self, csv_path: Path, db_path: Path, reports_dir: Path):
        self.csv_path = Path(csv_path)
        self.db_path = Path(db_path)
        self.reports_dir = Path(reports_dir)
        self.raw_data: pd.DataFrame | None = None
        self.cleaned_data: pd.DataFrame | None = None
        self.aggregated_data: pd.DataFrame | None = None

    def extract(self) -> pd.DataFrame:
        logger.info("EXTRACT: loading CSV from %s", self.csv_path)
        self.raw_data = pd.read_csv(self.csv_path)
        logger.info(
            "EXTRACT: loaded %s rows and %s columns",
            len(self.raw_data),
            len(self.raw_data.columns),
        )
        return self.raw_data

    def transform(self) -> pd.DataFrame:
        if self.raw_data is None:
            raise RuntimeError("extract() must be called before transform()")

        logger.info("TRANSFORM: cleaning raw dataset")
        df = self.raw_data.copy()

        numeric_columns = ["quantity", "price_per_unit"]
        text_columns = ["product_name", "category", "customer_name", "customer_city", "payment_method"]

        df = df.drop_duplicates()
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        for column in numeric_columns:
            median_value = df[column].median(skipna=True)
            df[column] = df[column].fillna(median_value)

        for column in text_columns:
            df[column] = df[column].fillna("Unknown")
            df[column] = df[column].replace("", "Unknown")

        df = df[(df["quantity"] > 0) & (df["price_per_unit"] > 0)]
        df = df.dropna(subset=["order_date"])

        df["total_amount"] = df["quantity"] * df["price_per_unit"]
        df["month_year"] = df["order_date"].dt.strftime("%Y-%m")

        self.cleaned_data = df.reset_index(drop=True)
        logger.info("TRANSFORM: %s rows after cleaning", len(self.cleaned_data))
        return self.cleaned_data

    def aggregate(self) -> pd.DataFrame:
        if self.cleaned_data is None:
            raise RuntimeError("transform() must be called before aggregate()")

        logger.info("AGGREGATE: grouping by category and month")
        grouped = (
            self.cleaned_data.groupby(["category", "month_year"], as_index=False)
            .agg(
                total_quantity=("quantity", "sum"),
                total_revenue=("total_amount", "sum"),
                avg_price=("price_per_unit", "mean"),
                order_count=("order_id", "nunique"),
            )
            .sort_values(["total_revenue", "category"], ascending=[False, True])
        )

        self.aggregated_data = grouped
        return self.aggregated_data

    def load_to_sqlite(self) -> None:
        if self.cleaned_data is None or self.aggregated_data is None:
            raise RuntimeError("transform() and aggregate() must be completed before load_to_sqlite()")

        logger.info("LOAD: writing tables to SQLite %s", self.db_path)
        engine = create_engine(f"sqlite:///{self.db_path}")
        self.cleaned_data.to_sql("sales_cleaned", engine, if_exists="replace", index=False)
        self.aggregated_data.to_sql("sales_aggregated", engine, if_exists="replace", index=False)

    def visualize(self) -> None:
        if self.aggregated_data is None:
            raise RuntimeError("aggregate() must be called before visualize()")

        self.reports_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="whitegrid")

        revenue_by_category = (
            self.aggregated_data.groupby("category", as_index=False)["total_revenue"].sum()
            .sort_values("total_revenue", ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=revenue_by_category, x="category", y="total_revenue", ax=ax)
        ax.set_title("Revenue by category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Revenue")
        fig.tight_layout()
        fig.savefig(self.reports_dir / "revenue_by_category.png")
        plt.close(fig)

        monthly_revenue = (
            self.aggregated_data.groupby("month_year", as_index=False)["total_revenue"].sum()
            .sort_values("month_year")
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=monthly_revenue, x="month_year", y="total_revenue", marker="o", ax=ax)
        ax.set_title("Monthly revenue")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        fig.tight_layout()
        fig.savefig(self.reports_dir / "monthly_revenue.png")
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            revenue_by_category["total_revenue"],
            labels=revenue_by_category["category"],
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.set_title("Revenue share by category")
        fig.tight_layout()
        fig.savefig(self.reports_dir / "revenue_share.png")
        plt.close(fig)

    def run(self) -> dict[str, pd.DataFrame]:
        logger.info("Running ETL pipeline")
        self.extract()
        self.transform()
        self.aggregate()
        self.load_to_sqlite()
        self.visualize()
        return {
            "raw": self.raw_data,
            "cleaned": self.cleaned_data,
            "aggregated": self.aggregated_data,
        }
