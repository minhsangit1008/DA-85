import pandas as pd
import numpy as np
from collections import defaultdict
import json

def preprocess_online_retail_ii(input_file, output_transactions, output_weights):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(input_file)
    
    # Đổi tên cột để khớp với logic script
    df = df.rename(columns={
        'Invoice': 'InvoiceNo',
        'Customer ID': 'CustomerID',
        'Price': 'UnitPrice'
    })
    
    # Chuyển InvoiceNo về kiểu chuỗi và xử lý giá trị thiếu
    df['InvoiceNo'] = df['InvoiceNo'].astype(str).fillna('0')
    
    # Làm sạch dữ liệu
    df = df.dropna(subset=['InvoiceNo', 'StockCode', 'CustomerID'])
    df = df[~df['InvoiceNo'].str.startswith('C')]  # Xóa hóa đơn hủy
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    
    # Chuyển thành định dạng giao dịch
    transactions = df.groupby('InvoiceNo')['StockCode'].apply(list).reset_index()
    transactions = transactions['StockCode'].tolist()
    
    # Lưu giao dịch với định dạng T1: ..., T2: ...
    with open(output_transactions, 'w') as f:
        for i, trans in enumerate(transactions, 1):
            f.write(f'T{i}: {" ".join(trans)}\n')
    
    # Tạo weight_dict dựa trên UnitPrice trung bình
    weight_dict = df.groupby('StockCode')['UnitPrice'].mean().to_dict()
    
    # Lưu weight_dict dưới dạng JSON trong file .txt
    with open(output_weights, 'w') as f:
        json.dump(weight_dict, f, indent=None, separators=(',', ':'))

if __name__ == "__main__":
    preprocess_online_retail_ii(
        input_file='online_retail_II.csv',
        output_transactions='transactions_online_retail_ii.txt',
        output_weights='weight_dict_online_retail_ii.txt'
    )