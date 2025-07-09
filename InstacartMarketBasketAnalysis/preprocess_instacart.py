import pandas as pd
import json

def preprocess_instacart(order_products_file, output_transactions, output_weights):
    # Đọc dữ liệu
    df = pd.read_csv(order_products_file)
    
    # Làm sạch dữ liệu
    df = df.dropna(subset=['order_id', 'product_id'])
    
    # Chuyển thành định dạng giao dịch
    transactions = df.groupby('order_id')['product_id'].apply(list).reset_index()
    transactions = transactions['product_id'].tolist()
    
    # Lưu giao dịch với định dạng T1: ..., T2: ...
    with open(output_transactions, 'w') as f:
        for i, trans in enumerate(transactions, 1):
            f.write(f'T{i}: {" ".join(map(str, trans))}\n')
    
    # Tạo weight_dict dựa trên tần suất xuất hiện (chuẩn hóa)
    weight_dict = df['product_id'].value_counts().to_dict()
    max_freq = max(weight_dict.values())
    weight_dict = {k: v/max_freq for k, v in weight_dict.items()}
    
    # Lưu weight_dict dưới dạng JSON trong file .txt
    with open(output_weights, 'w') as f:
        json.dump(weight_dict, f, indent=None, separators=(',', ':'))

if __name__ == "__main__":
    preprocess_instacart(
        order_products_file='order_products__prior.csv',
        output_transactions='transactions_instacart.txt',
        output_weights='weight_dict_instacart.txt'
    )