import pandas as pd
import os
import logging
import boto3
import csv

logging.basicConfig(level=logging.INFO)

LOCAL_ORDER_LISTS_PATH = "/tmp/order_lists"
LOCAL_DEFAULT_ORDER_LIST_PATH = "/tmp/data.csv"

BUCKET_NAME = "f35e4180-5bc7-4810-9403-95ab49618c83-eu-west-1"
OBJECT_KEY = "data.csv"


class OrderListManager:
    """Class to create, delete and rename csv files, which are order lists."""

    def __init__(self):
        self.s3 = boto3.client("s3")

    def read_default_list(self) -> pd.DataFrame:
        self.s3.download_file(BUCKET_NAME, OBJECT_KEY, LOCAL_DEFAULT_ORDER_LIST_PATH)
        dtype_spec = {"id": str, "name": str, "ean": str, "quantity": str}
        return pd.read_csv(LOCAL_DEFAULT_ORDER_LIST_PATH, dtype=dtype_spec)

    def write_default_list(self, df: pd.DataFrame) -> None:
        df.to_csv(LOCAL_DEFAULT_ORDER_LIST_PATH, index=False, quoting=csv.QUOTE_ALL)
        self.s3.upload_file(LOCAL_DEFAULT_ORDER_LIST_PATH, BUCKET_NAME, OBJECT_KEY)

    def exists_order_list(self, order_list_name: str):
        return os.path.exists(f"{LOCAL_ORDER_LISTS_PATH}/{order_list_name}.csv")

    def create_order_list(self):
        """Create a clean default order list."""
        df = pd.DataFrame(columns=["id", "name", "ean", "quantity"])
        self.write_default_list(df)
        logging.info(f"Default order list cleaned successfully!")

    def load_order_list(self, order_list_name: str) -> None:
        """
        Load a csv file to the default order list.
        Delete the csv file being loaded.
        """
        try:
            # check if it exists first
            # objects = self.s3.list_objects(BUCKET_NAME)
            DESIRED_OBJECT_KEY = f"{order_list_name}.csv"
            # if DESIRED_OBJECT_KEY not in objects:
            #     raise Exception(f"Order list '{order_list_name}' does not exist.")
            self.s3.download_file(
                BUCKET_NAME, DESIRED_OBJECT_KEY, LOCAL_DEFAULT_ORDER_LIST_PATH
            )
            self.s3.upload_file(LOCAL_DEFAULT_ORDER_LIST_PATH, BUCKET_NAME, OBJECT_KEY)
            self.s3.delete_object(BUCKET_NAME, f"{order_list_name}.csv")
        except Exception as e:
            logging.info(f"Order list '{order_list_name}' does not exist.")

    def save_order_list(self, order_list_name: str):
        """
        Save the current order list to a new csv file.
        Clean the default order list after saving it.
        """
        self.s3.download_file(BUCKET_NAME, OBJECT_KEY, LOCAL_DEFAULT_ORDER_LIST_PATH)
        self.s3.upload_file(
            LOCAL_DEFAULT_ORDER_LIST_PATH, BUCKET_NAME, f"{order_list_name}.csv"
        )
        self.create_order_list()
        logging.info(f"Order list '{order_list_name}' saved successfully.")

    def delete_order_list(self, order_list_name: str):
        try:
            os.remove(f"{LOCAL_ORDER_LISTS_PATH}/{order_list_name}.csv")
            logging.info(f"Order list '{order_list_name}' deleted successfully.")
        except FileNotFoundError:
            logging.info(f"Order list '{order_list_name}' does not exist.")

    def modify_order_list_name(self, old_name: str, new_name: str):
        try:
            os.rename(
                f"{LOCAL_ORDER_LISTS_PATH}/{old_name}.csv",
                f"{LOCAL_ORDER_LISTS_PATH}/{new_name}.csv",
            )
            logging.info(
                f"Order list '{old_name}' renamed to '{new_name}' successfully."
            )
        except FileNotFoundError:
            logging.info(f"Order list '{old_name}' does not exist.")
