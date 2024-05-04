import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(os.getcwd(), "..", "data")

ORDER_LISTS_PATH = os.path.join(DATA_PATH, "order_lists")

PRODUCTS_PATH = os.path.join(DATA_PATH, "products.csv")
DEFAULT_ORDER_LIST_PATH = os.path.join(DATA_PATH, "default_order_list.csv")


class OrderListManager:
    """Class to create, delete and rename csv files, which are order lists."""

    def exists_order_list(self, order_list_name: str):
        return os.path.exists(f"{ORDER_LISTS_PATH}/{order_list_name}.csv")

    def create_order_list(self):
        """Create a clean default order list."""
        df = pd.DataFrame(columns=["id", "name", "ean", "quantity"])
        df.to_csv(DEFAULT_ORDER_LIST_PATH, index=False)
        logging.info(f"Default order list cleaned successfully!")

    def load_order_list(self, order_list_name: str):
        """
        Load a csv file to the default order list.
        Delete the csv file being loaded.
        """
        try:
            df = pd.read_csv(f"{ORDER_LISTS_PATH}/{order_list_name}.csv")
            os.remove(f"{ORDER_LISTS_PATH}/{order_list_name}.csv")
            df.to_csv(DEFAULT_ORDER_LIST_PATH, index=False)
        except FileNotFoundError:
            logging.info(f"Order list '{order_list_name}' does not exist.")

    def save_order_list(self, order_list_name: str):
        """
        Save the current order list to a new csv file.
        Clean the default order list after saving it.
        """
        df = pd.read_csv(DEFAULT_ORDER_LIST_PATH)
        df.to_csv(f"{ORDER_LISTS_PATH}/{order_list_name}.csv", index=False)
        self.create_order_list()
        logging.info(f"Order list '{order_list_name}' saved successfully.")

    def delete_order_list(self, order_list_name: str):
        try:
            os.remove(f"{ORDER_LISTS_PATH}/{order_list_name}.csv")
            logging.info(f"Order list '{order_list_name}' deleted successfully.")
        except FileNotFoundError:
            logging.info(f"Order list '{order_list_name}' does not exist.")

    def modify_order_list_name(self, old_name: str, new_name: str):
        try:
            os.rename(
                f"{ORDER_LISTS_PATH}/{old_name}.csv",
                f"{ORDER_LISTS_PATH}/{new_name}.csv",
            )
            logging.info(
                f"Order list '{old_name}' renamed to '{new_name}' successfully."
            )
        except FileNotFoundError:
            logging.info(f"Order list '{old_name}' does not exist.")
