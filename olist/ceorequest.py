import pandas as pd
import numpy as np
from olist.data import Olist
from olist.order import Order


class Request:
    def __init__(self):
        # Import data only once
        olist = Olist()
        self.data = olist.get_data()
        self.order = Order()

    def get_seller_features(self):
        """
        Returns a DataFrame with:
        'seller_id'
        """
        sellers = self.data['sellers'][['seller_id']].copy()
        return sellers

    def get_active_dates(self):
        """
        Returns a DataFrame with:
        'seller_id', 'months_on_olist'
        """
        # First, get only orders that are approved
        orders_approved = self.data['orders'][[
            'order_id', 'order_approved_at'
        ]].dropna()

        # Then, create a (orders <> sellers) join table because a seller can appear multiple times in the same order
        orders_sellers = orders_approved.merge(self.data['order_items'],
                                               on='order_id')[[
                                                   'order_id', 'seller_id',
                                                   'order_approved_at'
                                               ]].drop_duplicates()
        orders_sellers["order_approved_at"] = pd.to_datetime(
            orders_sellers["order_approved_at"])

        # Compute dates
        orders_sellers["date_first_sale"] = orders_sellers["order_approved_at"]
        orders_sellers["date_last_sale"] = orders_sellers["order_approved_at"]
        df = orders_sellers.groupby('seller_id').agg({
            "date_first_sale": min,
            "date_last_sale": max
        })
        df['months_on_olist'] = round(
            (df['date_last_sale'] - df['date_first_sale']) /
            np.timedelta64(1, 'M')+1)
        df = df.drop(columns=['date_first_sale','date_last_sale'])
        return df

    def get_quantity(self):
        """
        Returns a DataFrame with:
        'seller_id', 'n_orders'
        """
        order_items = self.data['order_items']

        n_orders = order_items.groupby('seller_id')['order_id']\
            .nunique()\
            .reset_index()
        n_orders.columns = ['seller_id', 'orders']

        return n_orders

    def get_sales(self):
        """
        Returns a DataFrame with:
        'seller_id', 'sales'
        """
        return self.data['order_items'][['seller_id', 'price']]\
            .groupby('seller_id')\
            .sum()\
            .rename(columns={'price': 'sales'})

    def get_review_score(self):
        """
        Returns a DataFrame with:
        'seller_id', 'n_3_star_reviews',  'n_2_star_reviews',  'n_1_star_reviews'
        """
        sellers_2 = self.data['sellers'][['seller_id']].copy()
        order_items_2 = self.data['order_items'][['seller_id','order_id']].copy()
        orders_2 = self.data['orders'][['order_id']].copy()
        order_reviews = self.data['order_reviews'][['order_id','review_score']].copy()
        sellers_reviews = sellers_2.merge(order_items_2, on='seller_id')
        sellers_reviews = sellers_reviews.merge(orders_2, on='order_id')
        sellers_reviews = sellers_reviews.merge(order_reviews, on='order_id')

        three_star = sellers_reviews[sellers_reviews['review_score'] == 3].groupby('seller_id', as_index=False).count()
        three_star = three_star.drop(columns=['order_id'])
        three_star = three_star.rename(columns={'review_score':'3_star_reviews'})

        two_star = sellers_reviews[sellers_reviews['review_score'] == 2].groupby('seller_id', as_index=False).count()
        two_star = two_star.drop(columns=['order_id'])
        two_star = two_star.rename(columns={'review_score':'2_star_reviews'})

        one_star = sellers_reviews[sellers_reviews['review_score'] == 1].groupby('seller_id', as_index=False).count()
        one_star = one_star.drop(columns=['order_id'])
        one_star = one_star.rename(columns={'review_score':'1_star_reviews'})

        bad_reviews = three_star.merge(two_star, on='seller_id', how='left')
        bad_reviews = bad_reviews.merge(one_star, on='seller_id', how='left')
        return bad_reviews


    def get_data(self):
        """
        Returns a DataFrame with:
        ['seller_id','months_on_olist','n_orders','sales','n_3_star_reviews','n_2_star_reviews','n_1_star_reviews']
        """
        training_set =\
            self.get_seller_features()\
                .merge(
                self.get_active_dates(), on='seller_id', how='left'
               ).merge(
                self.get_quantity(), on='seller_id', how='left'
               ).merge(
                self.get_sales(), on='seller_id', how='left'
               ).merge(
                self.get_review_score(), on='seller_id', how='left')
        training_set = training_set.fillna(0)

        return training_set






#print(Request().get_data())
