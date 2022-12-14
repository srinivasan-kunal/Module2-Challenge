# Loan Qualifier Application Enhancement

This project aims to update the existing Loan Qualifier Application to allow the user to save the qualified loans to a CSV file.

User Story:
> "As a user, I need the ability to save the qualifying loans to a CSV file so that I can share the results as a spreadsheet."

---

## Technologies

Key python libraries required for the program: 

`fire` (0.3.1) 

`questionary` (1.5.2).

---

## Installation Guide

You can install Fire and Questionary from the Python Package Index (PyPI) using the following code 

```python
pip install fire
```

```python
pip install questionary
```
---

## Usage

The app can be initiated by a simple python command `python app.py`. It uses CLIs to get several other inputs from the user. 

The first user prompt is for the location and name of the "daily rate sheet". Input for this prompt must include the file name along with it's relative path (e.g. "./data/<'filename'>.csv"). The same may be used from the location [data](./data/). 

Next the application will prompt the user for details of the loan application like score, debt, income, loan value and property value. Based on the inputs eligible offers are pulled from the input data base. (details not shown here). 

In case there are no qualifying offers, the user will be notified and application will be exit. In case offers are available based on the values provided by the user there will be a prompt to save the results to a file. If confirmed by the user the application will prompt for an output file name (which must be provided along with the extension .csv). The application will print the file in the same location as the program i.e. the main directory.

The user will be exited from the application in four events
1) The input rate file does not exist (not shown in the code below)
2) There are no qualifying loan offers
3) The user decides not to save the results
4) The user accidentally provides the input path and file name when prompted for output file name

```python
    if len(qualifying_loans) == 0:
        print(f"Sorry! No offers were found to match your requirement at this time")
        sys.exit()
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
            else:
                print_csv(output_path,qualifying_loans)
```

As an extension, a feature has been added at the prompt of result file name which prevents a new user from accidentally using the input file name and location for the output. In the present version this event will result in a warning and exit the application. Further improvements may be made to this feature in the furture.

---

## Contributors


Kunal Srinivasan

---

## License

2022 edX Bootcamps 