from datetime import datetime


# Convert date strings to datetime objects for sorting
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y")
    except Exception:
        return datetime.min  # fallback for invalid/missing dates