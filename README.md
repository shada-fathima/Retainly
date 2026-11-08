# Retainly

Retainly is a customer retention analytics project.

## Purpose
Analyze customer data to identify churn patterns and retention opportunities.

## Setup
1. Activate the virtual environment:
   .\.venv\Scripts\Activate.ps1
2. Install dependencies:
   pip install -r requirements.txt

# Retainly

A customer-retention analytics project using the Online Retail II dataset.

## What it does

- Cleans transaction data from two Excel worksheets
- Calculates customer recency, frequency, and monetary value (RFM)
- Assigns rule-based customer segments
- Measures monthly paid repeat purchasing by cohort
- Displays results in an interactive Streamlit dashboard
- Exports filtered customer lists

## Dataset and scope

- Source: Online Retail II, UCI Machine Learning Repository
- Original combined dataset: 1,067,371 transaction rows
- Transaction dates: December 2009–December 2011
- Paid customer-sales rows after cleaning: 779,425
- Customers with paid purchases: 5,878
- RFM snapshot date: 10 December 2011

## Main findings

- Champions represent 17.27% of paying customers and
  57.99% of recorded positive-sales value.
- Champions and Loyal customers together represent 32.36%
  of customers and 75.81% of positive-sales value.
- The At-risk valuable segment contains 1,076 customers,
  with a median recency of 265 days.
- Weighted Month-1 paid repeat-purchase rate: 21.05%.
- Weighted Month-12 paid repeat-purchase rate: 18.39%.

## Methodology

### Cleaning

Exact duplicate rows were removed as a documented cleaning assumption.
Customer-level paid-purchase analysis excludes missing customer IDs,
cancellation invoices, non-positive quantities, and non-positive prices.

### RFM analysis

- Recency: calendar days since the last observed paid purchase
- Frequency: number of distinct paid-purchase invoices
- Monetary value: sum of quantity multiplied by price

Four-level scores and explicit rules assign customer segments.

### Cohort analysis

Customers are grouped by their first observed paid-purchase month.
Each follow-up rate measures purchasing in that specific calendar month.

The December 2009 boundary cohort is excluded from headline rates.
The incomplete December 2011 period is excluded from cohort analysis.
Only cohorts with complete follow-up are included in each headline rate.

## Limitations

- This is historical analysis, not a live customer-monitoring system.
- Segment labels are exploratory rules, not validated churn predictions.
- Monetary value excludes refunds and is not net revenue or profit.
- First observed purchase is not necessarily true acquisition.
- Identical transaction rows may sometimes represent legitimate repeated
  lines; removing them is an assumption, not proof of data error.
- Different follow-up rates use different eligible cohorts.
- Inactivity in a specific month does not establish permanent churn.
- Customer IDs are pseudonymous identifiers, not contact details.

## Project structure

- app.py: Streamlit dashboard
- notebooks/: loading, cleaning, RFM, and cohort analysis
- data/raw/: original workbook
- data/processed/: cleaned data and analysis outputs
- reports/figures/: exported charts

## Run locally

From the project root in Windows PowerShell:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

The processed CSV files must be present in data/processed.
To regenerate them, run the notebooks in numbered order.