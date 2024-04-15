# Competitor Price Monitor

**Client:** GadgetBazaar — electronics retailer
**Delivered:** April 2024
**Fee:** $150

## The Problem
Client needed daily visibility into a competitor's pricing but had no way to automatically track changes.

## My Solution
Built a Python script that scrapes a competitor's website daily, compares prices against the client's own catalog, and flags products where the client is more expensive. Outputs a timestamped CSV report.

## Tech Stack
- Python 3.x
- Pandas
- Requests & BeautifulSoup4

## How to Run
```bash
pip install -r requirements.txt
python generate_client_prices.py
python price_monitor.py
```

## Results
- Report automatically saves as `price_comparison_YYYY-MM-DD.csv`
- Client receives alert if any product is priced above competitor
