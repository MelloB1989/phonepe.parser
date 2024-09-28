import fitz  # PyMuPDF
import re

# Function to parse the extracted text into structured data
def parse_bank_statement(text):
    transactions = []
    lines = text.splitlines()

    # Regex patterns to match relevant parts of the data
    date_pattern = re.compile(r'^[A-Za-z]+\s\d{1,2},\s\d{4}')  # Matches dates like Sep 28, 2024
    amount_pattern = re.compile(r'₹[\d,]+(\.\d+)?')  # Matches amounts like ₹65
    debit_credit_pattern = re.compile(r'(DEBIT|CREDIT)')

    current_transaction = {}
    for line in lines:
        # Detect date to identify the start of a new transaction
        if date_pattern.match(line):
            if current_transaction:  # Save the previous transaction if it exists
                transactions.append(current_transaction)
                current_transaction = {}
            current_transaction['Date'] = line.strip()

        # Capture the time and transaction details
        elif re.match(r'\d{1,2}:\d{2}\s(am|pm)', line):
            current_transaction['Time'] = line.strip()

        # Capture the transaction details and type
        elif 'Paid to' in line or 'Received from' in line:
            current_transaction['Transaction Details'] = line.strip()

        elif debit_credit_pattern.search(line):
            current_transaction['Type'] = debit_credit_pattern.search(line).group()

        # Capture the amount
        elif amount_pattern.search(line):
            current_transaction['Amount'] = float((amount_pattern.search(line).group()).replace('₹', '').replace(',', ''))

        # Capture the transaction ID
        elif 'Transaction ID' in line:
            current_transaction['Transaction ID'] = line.split('Transaction ID')[-1].strip()

        # Capture the UTR number
        elif 'UTR No.' in line:
            current_transaction['UTR No.'] = line.split('UTR No.')[-1].strip()

        # Capture paid by details
        elif 'Paid by' in line:
            current_transaction['Paid By'] = line.split('Paid by')[-1].strip()

    # Append the last transaction if it exists
    if current_transaction:
        transactions.append(current_transaction)

    return transactions

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    with fitz.open(pdf_file) as pdf:
        text = ""
        for page_num in range(len(pdf)):
            text += pdf.load_page(page_num).get_text()
    return text

# Main function to parse the bank statement PDF
def main():
    pdf_file = 'phonepe.pdf'  # Replace with the path to your PDF file
    text = extract_text_from_pdf(pdf_file)
    transactions = parse_bank_statement(text)
    per_transactions = {}
    per_day = {}
    per_month = {}

    # Print the parsed transactions
    # for transaction in transactions:
    #     print(transaction)

    # save transactions in a json file
    import json
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f)
        print('transactions saved in transactions.json')

if __name__ == "__main__":
    main()
