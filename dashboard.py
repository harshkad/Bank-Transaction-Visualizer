import streamlit as st
import pandas as pd
import re
import io

# This "brain" remains the same.
CATEGORY_MAP = {
    # Food & Coffee
    'STARBUCKS': 'Food & Coffee',
    'ZOMATO': 'Food & Coffee',
    'CAFE COFFEE DAY': 'Food & Coffee',
    'SUBWAY': 'Food & Coffee',
    'MCDONALDS': 'Food & Coffee',

    # Groceries
    'SWIGGY INSTAMART': 'Groceries',
    'BIGBASKET': 'Groceries',
    'D-MART': 'Groceries',
    'BLINKIT': 'Groceries',
    'LOCAL SUPERMART': 'Groceries',

    # Transport
    'UBER': 'Transport',
    'OLA CABS': 'Transport',
    'RAPIDO': 'Transport',
    'DELHI METRO': 'Transport',
    
    # Bills & Utilities
    'PAYTM BILL PAY': 'Bills & Utilities',
    'BSES YAMUNA POWER': 'Bills & Utilities',
    'VODAFONE IDEA': 'Bills & Utilities',
    'AIRTEL PREPAID': 'Bills & Utilities',
    'MTNL DELHI': 'Bills & Utilities',

    # Subscriptions
    'NETFLIX': 'Subscriptions',
    'SPOTIFY AB': 'Subscriptions',
    'GOOGLE PLAY': 'Subscriptions',
    'AMAZON PRIME': 'Subscriptions',
    'DISNEY+ HOTSTAR': 'Subscriptions',
    'THE HINDU NEWS': 'Subscriptions',

    # Shopping
    'AMAZON SVCS': 'Shopping',
    'FLIPKART': 'Shopping',
    'MYNTRA': 'Shopping',
    'ZARA': 'Shopping',
    'H&M': 'Shopping',
    'DELL INDIA': 'Tech/Hardware',
    
    # Housing
    'PROPERTY RENTALS': 'Housing',
    'IKEA': 'Housing',

    # Fuel & Auto
    'SHELL PETROL': 'Fuel & Auto',
    'INDIAN OIL': 'Fuel & Auto',
    'MARUTI SUZUKI SVC': 'Fuel & Auto',
    
    # Health & Wellness
    'APOLLO PHARMACY': 'Health & Wellness',
    'CULT FIT': 'Health & Wellness',
    'NETMEDS': 'Health & Wellness',

    # Entertainment
    'BOOKMYSHOW': 'Entertainment',
    'PVR CINEMAS': 'Entertainment',
    
    # Travel
    'AIRBNB': 'Travel',
    'MAKE MY TRIP': 'Travel',
    'GOIBIBO': 'Travel',
    'INDIGO FLIGHT': 'Travel',
    
    # Income
    'SALARY': 'Income',
    'FREELANCE INVOICE': 'Income',

    # Refunds & Misc
    'REFUND': 'Refunds/Reimbursements',
    'CASHBACK': 'Refunds/Reimbursements',
    
    # Finance
    'ATM WITHDRAWAL': 'Bank/Finance',
    'BANK FEE': 'Bank/Finance',
}

def format_indian_currency(number):
    """Formats a number into the Indian numbering system (lakhs, crores)."""
    # First, get the number as a string with 2 decimal places
    s = f"{number:.2f}"
    
    # Split into integer and decimal parts
    parts = s.split('.')
    integer_part = parts[0]
    decimal_part = parts[1]

    # Handle negative numbers
    sign = ""
    if integer_part.startswith('-'):
        sign = "-"
        integer_part = integer_part[1:] # remove sign for processing

    # Format the integer part
    l = len(integer_part)
    if l <= 3:
        # No formatting needed for 3 digits or less
        formatted_integer = integer_part
    else:
        # Get the last 3 digits
        last_three = integer_part[-3:]
        # Get all other digits
        other_digits = integer_part[:-3]
        
        # Add a comma every 2 digits to 'other_digits'
        # We reverse the string, add commas, then reverse it back
        other_digits_with_commas = ','.join([other_digits[max(i-2, 0):i] for i in range(len(other_digits), 0, -2)][::-1])
        
        formatted_integer = other_digits_with_commas + ',' + last_three

    # Combine all parts and return
    return f"₹{sign}{formatted_integer}.{decimal_part}"


# The parsing functions remain exactly the same
def parse_transaction(email_body):
    # (This function is unchanged from the previous version)
    amount_re = re.search(r"(Rs\.|INR|\$)\s*([\d,]+\.?\d{2})", email_body)
    date_re = re.search(r"on\s+(\d{1,2}-[A-Za-z]{3}-\d{4})", email_body, re.IGNORECASE)
    type_ = "Debit"
    if "credit" in email_body.lower() or "received" in email_body.lower() or "credited" in email_body.lower():
        type_ = "Credit"
    vendor = "Other"
    email_upper = email_body.upper()
    for key in CATEGORY_MAP.keys():
        if key in email_upper:
            vendor = key
            break
    if type_ == "Credit" and "SALARY" in email_upper:
        vendor = "SALARY"
    if type_ == "Credit" and "REFUND" in email_upper:
        vendor = "REFUND"
    if type_ == "Credit" and "FREELANCE" in email_upper:
        vendor = "FREELANCE INVOICE"
            
    if amount_re and date_re:
        amount_str = amount_re.group(2).replace(",", "")
        amount = float(amount_str)
        date = date_re.group(1).upper()
        
        return {"date": date, "vendor": vendor, "amount": amount, "type": type_}
    return None

def process_data(raw_data_list):
    # (This function is unchanged from the previous version)
    processed_data = []
    for email in raw_data_list:
        # Skip empty lines in the text file
        if email.strip():
            data = parse_transaction(email)
            if data:
                processed_data.append(data)
    
    if not processed_data:
        return pd.DataFrame(columns=["date", "vendor", "amount", "type", "category"])

    df = pd.DataFrame(processed_data)
    df['category'] = df['vendor'].map(CATEGORY_MAP).fillna('Other')
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%Y')
    df = df.sort_values(by='date')
    return df

st.set_page_config(layout="wide")
st.title("Bank Transaction Visualizer (from .txt file)")

# --- NEW FILE UPLOADER WIDGET ---
uploaded_file = st.file_uploader("Upload your transactions.txt file", type=["txt"])

# --- Main logic ---
# Only run the dashboard code IF a file has been uploaded
if uploaded_file is not None:
    
    # 1. Read and process the file
    # To read file as string:
    string_io = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    # Read the string data and split it into a list by newlines
    raw_data_list = string_io.read().splitlines()

    # 2. Process the data (using the same function as before)
    df = process_data(raw_data_list)

    # 3. Separate expenses and income
    expenses_df = df[df['type'] == 'Debit'].copy()
    income_df = df[df['type'] == 'Credit'].copy()

    # --- Build the Dashboard ---
    
   # 4. Key Metrics
    st.header("Key Metrics")
    total_spent = expenses_df['amount'].sum()
    total_income = income_df['amount'].sum()
    net_flow = total_income - total_spent

    m1, m2, m3 = st.columns(3)
    # Use the new formatting function
    m1.metric("Total Spent", format_indian_currency(total_spent))
    m2.metric("Total Income", format_indian_currency(total_income))
    m3.metric("Net Cash Flow", format_indian_currency(net_flow))
    st.divider()

    # 5. Charts
    st.header("Expense Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        category_spending = expenses_df.groupby('category')['amount'].sum()
        st.bar_chart(category_spending)

    with col2:
        st.subheader("Spending Over Time")
        daily_spending = expenses_df.set_index('date').resample('D')['amount'].sum()
        st.line_chart(daily_spending)

    st.divider()

    # 6. Raw Data Tables
    st.header("Processed Data & Raw Logs")
    tab1, tab2 = st.tabs(["Processed DataFrame", "Raw Data from File"])

    with tab1:
        st.subheader("Processed & Categorized Transactions")
        st.dataframe(df)

    with tab2:
        st.subheader("Raw Text Data from Uploaded File")
        # Display the raw list of strings we read from the file
        st.json(raw_data_list)
        
else:
    # This message shows when no file is uploaded
    st.info("Please upload a .txt file to get started.")
