import pandas as pd

chunks = pd.read_csv('data.csv', chunksize=100000, encoding='ISO-8859-1')
lista = ['invoice_id', 'product_id', 'product_description', 'Quantity',
         'InvoiceDate', 'InvoiceTime', 'UnitPrice', 'CustomerID', 'Country']
df_total = pd.DataFrame(columns=lista)

for chunk in chunks:
    df_total = pd.concat([df_total, chunk])

print(df_total.shape)
# df_total['invoice_id'] = df_total['invoice_id'].astype('int64')
print(df_total['invoice_id'].value_counts())
print(df_total.dtypes)
