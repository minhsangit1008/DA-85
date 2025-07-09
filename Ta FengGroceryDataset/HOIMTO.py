from collections import defaultdict
import time
import psutil
import os
import pandas as pd
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, filename='result-HOIMTO.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_database(file_path):
    database = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if ':' in line:
                    items_part = line.strip().split(":", 1)[1]  
                    items = items_part.strip().split()  
                    database.append(set(items))
        logging.info(f"Successfully loaded database from {file_path}")
    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
        print(f"Error: File '{file_path}' not found.")
        return []
    return database

# Tính Transaction Occupancy (TO)
def calculate_TO(database):
    if not database:
        logging.error("Database is empty.")
        return []
    total_items = sum(len(t) for t in database)
    return [len(t) / total_items for t in database]

# Tính Itemset Occupancy (IO) và IOUB
def calculate_IO_IOUB(itemset, database, TO):
    if not database or not TO:
        logging.error("Database or TO is empty.")
        return 0.0, 0.0, []
    tids = [tid for tid, t in enumerate(database) if set(itemset).issubset(t)]
    IO = sum(TO[tid] for tid in tids) if tids else 0.0
    IOUB_tids = [tid for tid, t in enumerate(database) if any(item in t for item in itemset)]
    IOUB = sum(TO[tid] for tid in IOUB_tids) if IOUB_tids else 0.0
    return IO, IOUB, tids

# Thuật toán HOIMTO
def HOIMTO(database, MinIO):
    TO = calculate_TO(database)
    HOI = []
    
    # Tính tần suất cho 1-itemsets
    item_support = defaultdict(list)
    for tid, t in enumerate(database):
        for item in t:
            item_support[item].append(tid)
    logging.info(f"Number of initial items: {len(item_support)}")
    
    # Kiểm tra 1-itemsets
    candidates = [[item] for item in item_support]
    k = 1
    while candidates:
        next_candidates = []
        for itemset in candidates:
            IO, IOUB, tids = calculate_IO_IOUB(itemset, database, TO)
            logging.debug(f"Itemset: {itemset}, IO: {IO:.3f}, IOUB: {IOUB:.3f}")
            if IOUB >= MinIO:  # Cắt tỉa dựa trên IOUB
                if IO >= MinIO:
                    HOI.append((itemset, IO))
                    logging.info(f"Added itemset: {itemset}, IO: {IO:.3f}, IOUB: {IOUB:.3f}")
                # Sinh k+1 itemsets
                if k == 1:
                    next_candidates.extend([[itemset[0], new_item] for new_item in item_support if new_item > itemset[0]])
                else:
                    for other in candidates:
                        if other[:k-1] == itemset[:k-1] and other[k-1] > itemset[k-1]:
                            next_candidates.append(itemset + [other[k-1]])
        candidates = next_candidates
        k += 1
    
    return HOI

# Đo bộ nhớ
def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024  # MB
    logging.debug(f"Memory measured: {mem:.5f} MB")
    return mem

# Chạy thử và lưu kết quả
def tune_parameters(transactions_file):
    database = load_database(transactions_file)
    if not database:
        return

    min_io_values = [0.5]  # Thử nghiệm nhiều ngưỡng MinIO
    results = []

    for min_io in min_io_values:
        logging.info(f"Testing MinIO={min_io}")
        print(f"\nTesting MinIO={min_io}")
        
        start_time = time.time()
        start_memory = get_memory_usage()
        hoimto_results = HOIMTO(database, min_io)
        end_time = time.time()
        end_memory = get_memory_usage()
        
        num_itemsets = len(hoimto_results)
        time_taken = end_time - start_time
        memory_used = max(end_memory - start_memory, 0.0)
        
        results.append({
            'MinIO': min_io,
            'NumItemsets': num_itemsets,
            'Time(s)': time_taken,
            'Memory(MB)': memory_used
        })
        
        logging.info(f"Results: {num_itemsets} itemsets, {time_taken:.3f}s, {memory_used:.3f}MB")
        print(f"Found {num_itemsets} itemsets")
        print(f"Time: {time_taken:.3f} seconds")
        print(f"Memory: {memory_used:.3f} MB")
        if num_itemsets > 0:
            print("Top 5 itemsets:")
            for itemset, IO in hoimto_results[:5]:
                print(f"Itemset: {itemset}, IO: {IO:.3f}")

    try:
        results_df = pd.DataFrame(results)
        results_df.to_csv('result-HOIMTO.csv', index=False)
        logging.info("Results saved to result_step6.csv")
        print("\nResults saved to result_step6.csv")
    except Exception as e:
        logging.error(f"Failed to save CSV: {str(e)}")
        print(f"Error saving CSV: {str(e)}")

if __name__ == "__main__":
    transactions_file = "datatest.txt"
    tune_parameters(transactions_file)