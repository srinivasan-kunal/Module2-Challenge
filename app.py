# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import csv
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    # csvpath="./data/daily_rate_sheet.csv"
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """
    # credit_score=750
    # debt=5000 
    # income=20000 
    # loan_amount=100000
    # home_value=210000

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """

    #If there are no qualifying loans the application with exit with a message
    if len(qualifying_loans) == 0:
        print(f"Sorry! No offers were found to match your requirement at this time")
        sys.exit()

    # If there are qualifying loans available the application will prompt user to provide a file name
    # In case the user accidentally provides the location of the input file, it will prompt an error and 
    # ask to re-enter the file name 
    

    else:
        print(f"Congratulations! There are {int(len(qualifying_loans))} to select from.")
        save_csv=questionary.confirm("Would you like to save your result?").ask()
        if not save_csv:
            print(f"Thank you for your response. The results will not be saved.")
            sys.exit()

        elif save_csv:
            output_path=questionary.text("Please provide a name for the result file.").ask()
            if output_path=="./data/daily_rate_sheet.csv":
                 print(f"ERROR: Output file cannot be the same as input file. Please try again.")
                 sys.exit()

            # Set the output header
            header = ["Financial Institution", "Max Loan Amount", "Max Loan To Value", "Max Debt to Income Ratio", "Minumum Credit Score","APR Offered"]

            # Set the output file path
            result_path = Path(output_path)

            # Pulling the `csv.writer` from csv library to write the header row
            # and each row of qualifying loan from the `qualifying_loans` list.
            with open(result_path,'w',newline='') as csvfile:
                csvwriter=csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(header)
                for row in qualifying_loans:
                    csvwriter.writerow(row)

    #Verification code to open and review the new file created    
    # with open(result_path) as resultfile:
    #     data=csv.reader(resultfile)
    #     counter=0

    #     for rows in data:
    #         counter+=1

    #         if counter< 5:
    #             print(rows)
    #         else:
    #             sys.exit()
    #     print(f"Final count of data printed {counter}")
    return

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
