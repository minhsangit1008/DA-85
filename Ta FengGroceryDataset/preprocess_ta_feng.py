import pandas as pd
import json

def preprocess_ta_feng(input_file, output_transactions, output_weights):
    # Đọc dữ liệu CSV với ngày tháng
    df = pd.read_csv(input_file, parse_dates=["TRANSACTION_DT"])
    
    # Làm sạch dữ liệu
    df = df.dropna(subset=["CUSTOMER_ID", "PRODUCT_SUBCLASS"])
    df = df[df["AMOUNT"] > 0]
    
    # Đổi tên cột ngày để thuận tiện
    df.rename(columns={"TRANSACTION_DT": "DATE"}, inplace=True)

    # Chuyển thành định dạng giao dịch (nhóm theo CUSTOMER_ID và DATE)
    transactions = df.groupby(["CUSTOMER_ID", "DATE"])["PRODUCT_SUBCLASS"].apply(list).reset_index()
    transactions_list = transactions["PRODUCT_SUBCLASS"].tolist()

    # Lưu giao dịch với định dạng T1: ..., T2: ...
    with open(output_transactions, "w") as f:
        for i, trans in enumerate(transactions_list, 1):
            f.write(f"T{i}: {' '.join(map(str, trans))}\n")

    # Tạo weight_dict dựa trên tần suất xuất hiện (chuẩn hóa)
    weight_dict = df["PRODUCT_SUBCLASS"].value_counts().to_dict()
    max_freq = max(weight_dict.values())
    weight_dict = {k: v / max_freq for k, v in weight_dict.items()}

    # Lưu weight_dict dưới dạng JSON trong file .txt
    with open(output_weights, "w") as f:
        json.dump(weight_dict, f, indent=None, separators=(",", ":"))

if __name__ == "__main__":
    preprocess_ta_feng(
        input_file="ta_feng_all_months_merged.csv",
        output_transactions="transactions_ta_feng.txt",
        output_weights="weight_dict_ta_feng.txt"
    )
