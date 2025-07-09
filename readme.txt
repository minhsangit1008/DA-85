HOWI-MTO: High-Occupancy Weighted Itemset Mining on Multiple Retail Datasets
This project implements the HOWI-MTO (High-Occupancy Weighted Itemset Mining with Transaction Occupancy) algorithm to mine high-occupancy itemsets from four retail datasets: TaFeng, Online Retail, Online Retail II, and Instacart. Each dataset is processed using a dedicated preprocessing script and the main mining algorithm script (HOWI_MTO.py). Datasets are organized in separate directories for efficient management of input and output files.
Project Overview
The HOWI-MTO algorithm extends traditional High Occupancy Itemset Mining (HOIM) by incorporating item weights and transaction occupancy, utilizing an FP-Tree data structure for efficient computation. It discovers itemsets that are both frequent and significant in terms of weighted occupancy, making it ideal for retail basket analysis and other transactional data applications.
Each dataset has its own preprocessing script to generate transaction and weight files, followed by the HOWI-MTO algorithm to mine itemsets with varying thresholds (MinWIO and min_ws). Results, including the number of itemsets, execution time, and memory usage, are saved to CSV files and logged for analysis.
Prerequisites
To run the project, ensure you have the following installed:
* Python 3.6+
* Required Python libraries:
* pip install pandas psutil
Directory Structure
Each dataset is stored in a separate directory containing its input dataset, preprocessing script, mining script, and output files. Below is the structure for all datasets, with the Online Retail directory as an example (inspired by image.png):
DA-85/

DA-85/
├── OnlineRetail/
│   ├── online_retail.csv                    # Input dataset (Excel/CSV)
│   ├── preprocess_online_retail.py          # Preprocessing script for Online Retail
│   ├── HOWI_MTO.py                         # Mining algorithm script
│   ├── transactions_online_retail.txt       # Preprocessed transactions
│   ├── weight_dict_online_retail.txt        # Item weights in JSON format
│   ├── result_online_retail.csv             # Mining results
│   ├── result_online_retail.log             # Execution log
├── OnlineRetailII/
│   ├── online_retail_II.csv                 # Input dataset
│   ├── preprocess_online_retail_II.py       # Preprocessing script for Online Retail II
│   ├── HOWI_MTO.py                         # Mining algorithm script
│   ├── transactions_online_retail_II.txt    # Preprocessed transactions
│   ├── weight_dict_online_retail_II.txt     # Item weights in JSON format
│   ├── result_online_retail_II.csv          # Mining results
│   ├── result_online_retail_II.log          # Execution log
├── TaFeng/
│   ├── ta_feng_all_months_merged.csv        # Input dataset
│   ├── preprocess_ta_feng.py                # Preprocessing script for TaFeng
│   ├── HOWI_MTO.py                         # Mining algorithm script
│   ├── transactions_ta_feng.txt             # Preprocessed transactions
│   ├── weight_dict_ta_feng.txt              # Item weights in JSON format
│   ├── result_tafeng.csv                    # Mining results
│   ├── result_tafeng.log                    # Execution log
├── Instacart/
│   ├── order_products__prior.zip            # Input dataset
│   ├──order_products__prior.z01
│   ├──order_products__prior.z02
│   ├──order_products__prior.z03
│   ├── preprocess_instacart.py              # Preprocessing script for Instacart
│   ├── HOWI_MTO.py                         # Mining algorithm script
│   ├── transactions_instacart.txt           # Preprocessed transactions
│   ├── weight_dict_instacart.txt            # Item weights in JSON format
│   ├── result_instacart.csv                 # Mining results
│   ├── result_instacart.log                 # Execution log

Note: Because the order_products__prior.csv file is too large, please unzip it before running the program.
Usage
Step 1: Prepare the Datasets
Place the input datasets in their respective directories:
* TaFeng: TaFeng/ta_feng_all_months_merged.csv 
* Online Retail: OnlineRetail/online_retail.csv 
* Online Retail II: OnlineRetailII/online_retail_II.csv 
* Instacart: Instacart/order_products__prior.
Step 2: Preprocess the Datasets
Navigate to the dataset's directory and run the corresponding preprocessing script to generate transaction and weight files.
For TaFeng:
Navigate to the TaFeng directory:
cd TaFeng
python preprocess_ta_feng.py
For Online Retail:
Navigate to the OnlineRetail directory:
cd OnlineRetail
python preprocess_online_retail.py
For Online Retail II:
Navigate to the OnlineRetailII directory:
cd OnlineRetailII
python preprocess_online_retail_II.py
For Instacart:
Navigate to the Instacart directory:
cd Instacart
python preprocess_instacart.py
Step 3: Run the HOWI-MTO Algorithm
Navigate to the dataset's directory and run the HOWI-MTO algorithm by updating the file paths in HOWI_MTO.py.	
Example for Online Retail:
cd OnlineRetail
python HOWI_MTO.py
Repeat for other datasets:
* TaFeng:
* transactions_file = "transactions_ta_feng.txt"
* weights_file = "weight_dict_ta_feng.txt"
* Online Retail II:
* transactions_file = "transactions_online_retail_II.txt"
* weights_file = "weight_dict_online_retail_II.txt"
* Instacart:
* transactions_file = "transactions_instacart.txt"
* weights_file = "weight_dict_instacart.txt"
Configuration
The HOWI_MTO.py script tests multiple threshold combinations:
* MinWIO (Minimum Weighted Itemset Occupancy).
* min_ws (Minimum Weighted Support).
* Modify these values in the tune_parameters function to adjust the algorithm's behavior for each dataset.
Output
For each dataset, the following files are generated in their respective directories:
* Transactions File (e.g., transactions_online_retail.txt): Transactions in the format T1: item1 item2 ....
* Weights File (e.g., weight_dict_online_retail.txt): JSON file with item weights (e.g., {"85123A": 0.5, "71053": 0.3, ...}).
* Results File (e.g., result_online_retail.csv): Contains results for each threshold combination:
o Columns: MinWIO, min_ws, NumItemsets, Time(s), Memory(MB).
* Log File (e.g., result_online_retail.log): Logs detailed execution information, including FP-Tree structure, WIO/WIOUB values, and itemsets found.
Notes
* Ensure input datasets are placed in their respective directories and correctly formatted.
* Each preprocessing script (preprocess_ta_feng.py, preprocess_online_retail.py, preprocess_online_retail_II.py, preprocess_instacart.py) is tailored to its dataset's column structure.
* Memory usage may be reported as 0 MB for small datasets or high thresholds due to limitations in psutil measurements.
* To achieve more itemsets (e.g., 50 60), lower the thresholds (e.g., MinWIO=0.005, min_ws=0.005) or adjust weights in the respective weight files.
* The algorithm is optimized for retail datasets but can be adapted for other weighted transactional datasets.
Future Improvements
* Optimize memory usage for low thresholds, especially for large datasets like Instacart.
* Implement parallel processing to reduce execution time on large datasets.
* Develop a unified preprocessing script to handle diverse dataset formats automatically.
* Explore alternative data structures (e.g., bitmaps) for further efficiency.
Authors
* Nguy?n Minh Sang   520H0147
* Tr?n Thi n B?o   520H0517
* Advisor: Mr. Do n Xu n Thanh
Institution
Faculty of Information Technology, Ton Duc Thang University, Ho Chi Minh City, Vietnam

