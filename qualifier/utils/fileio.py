# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
from pathlib import Path

def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

def print_csv(filename,loan_offers):
    # Set the output header
    header = ["Financial Institution", "Max Loan Amount", "Max Loan To Value", "Max Debt to Income Ratio", "Minumum Credit Score","APR Offered"]
    # Set the output filename path
    result_path = Path(filename)
    # Pulling the `csv.writer` from csv library to write the header row
    # and each row of qualifying loan from the `qualifying_loans` list.
    with open(result_path,'w',newline='') as csvfile:
        csvwriter=csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(header)
        for row in loan_offers:
            csvwriter.writerow(row)
    return