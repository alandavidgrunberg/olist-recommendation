import os
import pandas as pd


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data','csv')

        file_names = ['olist_sellers_dataset.csv',
        'product_category_name_translation.csv',
        'olist_orders_dataset.csv',
        'olist_order_items_dataset.csv',
        'olist_customers_dataset.csv',
        'olist_geolocation_dataset.csv',
        'olist_order_payments_dataset.csv',
        'olist_order_reviews_dataset.csv',
        'olist_products_dataset.csv']

        key_names = ['sellers',
        'product_category_name_translation',
        'orders',
        'order_items',
        'customers',
        'geolocation',
        'order_payments',
        'order_reviews',
        'products']

        data_frames = []
        for file_name in file_names:
            csv = pd.read_csv(os.path.join(csv_path, file_name))
            data_frames.append(csv)

        data = {key_name:data_frame for key_name,data_frame in zip(key_names,data_frames)}


        return data





    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
