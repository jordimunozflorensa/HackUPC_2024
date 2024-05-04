import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(os.getcwd(), "data")

PRODUCTS_PATH = os.path.join(DATA_PATH, "products.csv")
DEFAULT_ORDER_LIST_PATH = os.path.join(DATA_PATH, "default_order_list.csv")


class OrderItemManager:

    def read_default_list(self) -> pd.DataFrame:
        return pd.read_csv(DEFAULT_ORDER_LIST_PATH)

    def write_default_list(self, df: pd.DataFrame) -> None:
        df.to_csv(DEFAULT_ORDER_LIST_PATH, index=False)

    def exists_item(self, df: pd.DataFrame, name: str) -> bool:
        try:
            return name in set(df["name"])
        except Exception as e:
            logging.error(f"Error while checking if item exists: {e}")
    
    def delete_item(self, prod_name: str, ean: str) -> None:
        try:
            df = self.read_default_list()
            row_index = df[df["ean"] == ean].index[0]
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
            logging.info(f"New item added successfully to '{DEFAULT_ORDER_LIST_PATH}'.")
        except Exception as e:
            logging.error(f"Error occurred while adding item: {e}")
