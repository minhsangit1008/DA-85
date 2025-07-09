import pandas as pd
import json

def preprocess_online_retail(input_file, output_transactions, output_weights, min_item_freq=5):
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(input_file)
    
    # Đổi tên cột nếu cần (đảm bảo thống nhất với dataset)
    df = df.rename(columns={
        'Invoice': 'InvoiceNo',
        'Customer ID': 'CustomerID',
        'Price': 'UnitPrice'
    })
    
    # Chuyển InvoiceNo và StockCode về kiểu chuỗi, xử lý giá trị thiếu
    df['InvoiceNo'] = df['InvoiceNo'].astype(str).fillna('0')
    df['StockCode'] = df['StockCode'].astype(str).str.upper()
    
    # Làm sạch dữ liệu
    df = df.dropna(subset=['InvoiceNo', 'StockCode', 'CustomerID', 'UnitPrice'])
    df = df[~df['InvoiceNo'].str.startswith('C')]  # Xóa hóa đơn hủy
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    
    # Loại bỏ mặt hàng hiếm
    item_counts = df['StockCode'].value_counts()
    valid_items = set(item_counts[item_counts >= min_item_freq].index)
    df = df[df['StockCode'].isin(valid_items)]
    
    # Tạo weight_dict dựa trên UnitPrice trung bình
    weight_dict = df.groupby('StockCode')['UnitPrice'].mean().to_dict()
    
    # Lưu weight_dict dưới dạng JSON
    with open(output_weights, 'w') as f:
        json.dump(weight_dict, f, indent=None, separators=(',', ':'))
    
    # Chuyển thành định dạng giao dịch
    transactions = df.groupby('InvoiceNo')['StockCode'].apply(list).reset_index()
    transaction_list = transactions['StockCode'].tolist()
    
    # Lưu giao dịch với định dạng T1: ..., T2: ..., chỉ giữ item trong weight_dict
    with open(output_transactions, 'w') as f:
        for i, trans in enumerate(transaction_list, 1):
            items = [item for item in trans if item in weight_dict]
            if items:
                f.write(f'T{i}: {" ".join(items)}\n')
    
    # Thống kê
    print(f"Weight dictionary saved to {output_weights}")
    print(f"Number of items in weight_dict: {len(weight_dict)}")
    print(f"Sample weights: {dict(list(weight_dict.items())[:5])}")
    print(f"\nTransactions saved to {output_transactions}")
    print(f"Number of transactions: {sum(1 for line in open(output_transactions))}")
    print(f"Number of unique items in transactions: {len(set(item for line in open(output_transactions) for item in line.strip().split(':')[1].split() if ':' in line))}")
    print(f"Sample transactions: {[line.strip() for line in open(output_transactions).readlines()[:5]]}")

if __name__ == "__main__":
    preprocess_online_retail(
        input_file='Online Retail.xlsx',
        output_transactions='online_retail_transactions.txt',
        output_weights='weight_dict.txt'
    )