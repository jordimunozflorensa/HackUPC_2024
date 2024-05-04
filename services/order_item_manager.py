import pandas as pd
import os
import logging
import boto3

logging.basicConfig(level=logging.INFO)

LOCAL_ORDER_LISTS_PATH = "/tmp/order_lists"
LOCAL_DEFAULT_ORDER_LIST_PATH = "/tmp/data.csv"

BUCKET_NAME = "f35e4180-5bc7-4810-9403-95ab49618c83-eu-west-1"
OBJECT_KEY = "data.csv"

class OrderItemManager:

    def __init__(self):
        self.s3 = boto3.client("s3")

    def read_default_list(self) -> pd.DataFrame:
        self.s3.download_file(BUCKET_NAME, OBJECT_KEY, LOCAL_DEFAULT_ORDER_LIST_PATH)
        return pd.read_csv(LOCAL_DEFAULT_ORDER_LIST_PATH)

    def write_default_list(self, df: pd.DataFrame) -> None:
        df.to_csv(LOCAL_DEFAULT_ORDER_LIST_PATH, index=False)
        self.s3.upload_file(LOCAL_DEFAULT_ORDER_LIST_PATH, BUCKET_NAME, OBJECT_KEY)

    def exists_item(self, df: pd.DataFrame, name: str) -> bool:
        try:
            return name in set(df["name"])
        except Exception as e:
            logging.error(f"Error while checking if item exists: {e}")
    
    def delete_item(self, prod_name: str) -> None:
        try:
            df = self.read_default_list()

            if not self.exists_item(df, prod_name):
                raise Exception(f"Item {prod_name} does not exist in the list.")

            row_index = df[df["name"] == prod_name].index[0]
            df.drop(index=row_index, inplace=True)
            self.write_default_list(df)
            logging.info(f"Item {prod_name} deleted successfully.")
        except Exception as e:
            logging.error(f"Error while deleting item: {e}")

    def modify_item(self, prod_name: str, new_qty: int) -> None:
        try:
            df = self.read_default_list()

            if not self.exists_item(df, prod_name):
                raise Exception(f"Item {prod_name} does not exist in the list.")
            
            df.loc[df["name"] == prod_name, "quantity"] = new_qty

            self.write_default_list(df)
            logging.info(f"Item {prod_name} modified to qty {new_qty} successfully.")
        except Exception as e:
            logging.error(f"Error while modifying item: {e}")


    def add_item(self, id: str, name: str, ean: str, qty: int) -> None:
        try:
            df = self.read_default_list()
            new_data = pd.DataFrame({"id": [id], "name": [name], "ean": [ean], "quantity": [qty]})
            
            if self.exists_item(df, name):
                raise Exception(f"Item {name} already exists in the list.")

            if all(df.columns == new_data.columns):
                df = pd.concat([df, new_data], ignore_index=True, axis=0)
            else:
                raise Exception("Columns of the new row don't match the DataFrame columns.")

            self.write_default_list(df)
            logging.info(f"New item added successfully to '{LOCAL_DEFAULT_ORDER_LIST_PATH}'.")
        except Exception as e:
            logging.error(f"Error occurred while adding item: {e}")
