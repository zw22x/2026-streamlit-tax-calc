# Tax App

A simple 2026 federal tax calculator built with Python and Streamlit.

This project lets you enter your income and filing status, then estimates:

- taxable income
- federal income tax
- effective tax rate
- the tax brackets used in the calculation

It also includes unit tests for the core tax calculation logic.

## Getting Started

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run dict_version.py
```

Streamlit will open the app in your browser.

## Run the Tests

```bash
python3 -m unittest tests/test_dict_version.py -v
```

## Project Files

- `dict_version.py` - Streamlit app and dictionary-based tax logic
- `main.py` - original command-line version
- `tests/test_dict_version.py` - unit tests for the tax calculator
- `requirements.txt` - Python dependencies

## Note

This calculator is for learning and educational use only. It is not tax advice.
