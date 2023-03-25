import pandas as pd
import os

dfs =[]

path = 'transactions'
for folder in os.listdir(path):
    # print(folder)
    f = os.path.join(path, folder)
    for json_file in os.listdir(f):
        # print(json_file)
        data = pd.read_json(json_file, lines= True)
        dfs.append(data)
df_transactions = pd.concat(dfs, ignore_index=True)

df_transactions_1 = df_transactions.explode('basket')
df_transactions_2 = pd.concat([df_transactions_1.drop(['basket'], axis=1), df_transactions_1['basket'].apply(pd.Series)], axis=1)


df_customers = pd.read_csv('customers.csv')
df_products = pd.read_csv('products.csv')
df_transactions = pd.read_json('transactions.json', lines=True)

df_2 = pd.merge(df_customers, df_transactions_2, left_on='customer_id', right_on='customer_id')
df_3 = pd.merge(df_2, df_products, left_on='product_id', right_on='product_id')

df_4 = df_3.groupby(['customer_id', 'loyalty_score', 'product_id', 'product_category','date_of_purchase'])['customer_id'].count().reset_index(name='purchase_count')

df_final = df_4[['customer_id', 'loyalty_score', 'product_id', 'product_category','purchase_count']]

df_final.to_json('output.json')