# 📊 Bank Transaction Visualizer

**A Python web application that turns raw text alerts from your bank into an interactive financial dashboard.**

## 📖 About The Project

Managing finances by reading through hundreds of unstructured SMS or email alerts is tedious and difficult. This tool automates that process. You simply upload a text file containing your raw transaction alerts, and the application parses, cleans, and visualizes your spending habits instantly.

## ✨ Key Features

* **Automated Parsing:** Uses advanced pattern matching (Regex) to extract dates, amounts, and vendor names from messy text.
* **Smart Categorization:** Automatically organizes transactions into clear categories like 'Food & Coffee', 'Groceries', and 'Transport'.
* **Indian Currency Formatting:** Features a custom formatter to display numbers in the Indian system (Lakhs and Crores) for better readability.
* **Interactive Dashboard:** view key metrics (Total Spent, Net Flow), spending trends over time, and category breakdowns.

## ⚙️ How It Works

The application runs as a linear data pipeline:

1.  **Upload:** You drag and drop your `transactions.txt` file into the web interface.
2.  **Read & Parse:** The script reads the file line-by-line and uses Regular Expressions to extract structured data _(date, amount, vendor, type)_ from the raw text.
3.  **Process:** The data is loaded into Pandas, where it is cleaned, and vendors are mapped to specific spending categories.
4.  **Visualize:** Streamlit uses the processed data to render interactive charts and summary metrics on your screen.

## 🛠️ Technologies Used

* **Python 3:** The core programming language.
* **Streamlit:** Used to build the user interface and interactive dashboard.
* **Pandas:** Handles all data structuring, cleaning, and aggregation.
* **re (Regular Expressions):** The built-in Python module used as the parsing engine to "read" the text alerts.

## 🚀 Quick Start

### Prerequisites

* Python 3.x installed on your system.

### Installation & Run

1.  Clone this repository:
    ```bash
    git clone [https://github.com/harshkad/bank-transaction-visualizer.git](https://github.com/harshkad/bank-transaction-visualizer.git)
    ```
2.  Install the required packages:
    ```bash
    pip install streamlit pandas
    ```
3.  Run the application:
    ```bash
    streamlit run dashboard.py
    ```

The application will open automatically in your web browser at `http://localhost:8501`.
