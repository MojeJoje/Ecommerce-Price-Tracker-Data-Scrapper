"""Process and export product data to various formats."""

import logging
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and export product data."""

    def __init__(self, output_dir: Path):
        """
        Initialize DataProcessor.

        Args:
            output_dir: Directory where output files will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_dataframe(self, products: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Convert product list to pandas DataFrame.

        Args:
            products: List of product dictionaries

        Returns:
            pandas DataFrame with product data
        """
        if not products:
            logger.warning("No products to convert to DataFrame")
            return pd.DataFrame()

        df = pd.DataFrame(products)
        df["scraped_at"] = datetime.now()
        return df

    def save_to_csv(
        self, products: List[Dict[str, Any]], filename: str = "products.csv"
    ) -> Path:
        """
        Save products to CSV file.

        Args:
            products: List of product dictionaries
            filename: Output filename

        Returns:
            Path to saved file
        """
        df = self.to_dataframe(products)
        output_path = self.output_dir / filename

        df.to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"Saved {len(products)} products to {output_path}")
        return output_path

    def save_to_excel(
        self,
        products: List[Dict[str, Any]],
        filename: str = "products.xlsx",
        sheet_name: str = "Products",
    ) -> Path:
        """
        Save products to Excel file.

        Args:
            products: List of product dictionaries
            filename: Output filename
            sheet_name: Name of the Excel sheet

        Returns:
            Path to saved file
        """
        df = self.to_dataframe(products)
        output_path = self.output_dir / filename

        # Create Excel writer with formatting
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Format columns
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        logger.info(f"Saved {len(products)} products to {output_path}")
        return output_path

    def save_price_history(
        self,
        products: List[Dict[str, Any]],
        filename: str = "price_history.xlsx",
    ) -> Path:
        """
        Save price history with comparison data.

        Args:
            products: List of product dictionaries
            filename: Output filename

        Returns:
            Path to saved file
        """
        df = self.to_dataframe(products)

        # Add price change tracking columns
        df["previous_price"] = None
        df["price_change"] = None
        df["change_percentage"] = None

        output_path = self.output_dir / filename

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Price History", index=False)

        logger.info(f"Saved price history to {output_path}")
        return output_path

    def merge_product_data(
        self, *product_lists: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge multiple product lists.

        Args:
            *product_lists: Variable number of product lists

        Returns:
            Merged product list
        """
        merged = []
        for products in product_lists:
            merged.extend(products)

        # Remove duplicates based on product name and source
        seen = set()
        unique_products = []
        for product in merged:
            key = (product.get("name"), product.get("source"))
            if key not in seen:
                seen.add(key)
                unique_products.append(product)

        logger.info(f"Merged {len(merged)} products into {len(unique_products)} unique products")
        return unique_products

    def filter_products(
        self,
        products: List[Dict[str, Any]],
        in_stock_only: bool = False,
        min_price: float = None,
        max_price: float = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter products based on criteria.

        Args:
            products: List of products to filter
            in_stock_only: Filter to in-stock products only
            min_price: Minimum price filter
            max_price: Maximum price filter

        Returns:
            Filtered product list
        """
        filtered = products

        if in_stock_only:
            filtered = [p for p in filtered if p.get("in_stock", False)]

        if min_price is not None:
            filtered = [
                p
                for p in filtered
                if self._parse_price(p.get("price")) >= min_price
            ]

        if max_price is not None:
            filtered = [
                p
                for p in filtered
                if self._parse_price(p.get("price")) <= max_price
            ]

        logger.info(f"Filtered {len(products)} products to {len(filtered)} products")
        return filtered

    @staticmethod
    def _parse_price(price_str: str) -> float:
        """Extract numeric price from string."""
        try:
            return float(price_str.replace("$", "").replace(",", ""))
        except (ValueError, AttributeError):
            return 0.0
