"""
Fraud Detection Sample Data Generator
Generates realistic banking fraud detection data with ~5% suspicious transactions.
Outputs: customers.csv, bankaccounts.csv, merchants.csv, transactions.csv
"""

import csv
import os
import random
import string
from datetime import datetime, timedelta, timezone

try:
    from faker import Faker
    fake = Faker()
    Faker.seed(42)
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False
    print("Warning: faker not installed. Using built-in fallback data generation.")
    print("Install faker for better data: pip install faker\n")

random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now(timezone.utc).replace(tzinfo=None)

# ---------------------------------------------------------------------------
# Fallback data pools (used when faker is not available)
# ---------------------------------------------------------------------------
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Lisa", "Matthew", "Nancy",
    "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra", "Steven", "Ashley",
    "Paul", "Dorothy", "Andrew", "Kimberly", "Joshua", "Emily", "Kenneth", "Donna",
    "Kevin", "Michelle", "Brian", "Carol", "George", "Amanda", "Timothy", "Melissa",
    "Ronald", "Deborah", "Edward", "Stephanie", "Jason", "Rebecca", "Jeffrey", "Sharon",
    "Ryan", "Laura", "Jacob", "Cynthia", "Gary", "Kathleen", "Nicholas", "Amy",
    "Eric", "Angela", "Jonathan", "Shirley", "Stephen", "Anna", "Larry", "Brenda",
    "Justin", "Pamela", "Scott", "Emma", "Brandon", "Nicole", "Benjamin", "Helen",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
]

STREETS = [
    "Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine St", "Elm St", "Washington Blvd",
    "Park Ave", "Lake Dr", "Hill Rd", "River Rd", "Sunset Blvd", "Broadway", "Church St",
    "Spring St", "Market St", "Center St", "Union Ave", "Franklin St", "Highland Ave",
]

CITIES_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
    ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
    ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("Indianapolis", "IN"),
    ("San Francisco", "CA"), ("Seattle", "WA"), ("Denver", "CO"), ("Nashville", "TN"),
    ("Oklahoma City", "OK"), ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"),
    ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"),
    ("Tucson", "AZ"), ("Fresno", "CA"), ("Mesa", "AZ"), ("Sacramento", "CA"),
    ("Atlanta", "GA"), ("Kansas City", "MO"), ("Omaha", "NE"), ("Miami", "FL"),
    ("Minneapolis", "MN"), ("Cleveland", "OH"), ("Tampa", "FL"), ("Boston", "MA"),
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com",
    "icloud.com", "mail.com", "protonmail.com", "live.com", "msn.com",
]

# Merchant name templates per category
MERCHANT_TEMPLATES = {
    "Retail": ["QuickBuy", "MegaMart", "ValueShop", "BargainBox", "SmartSave", "DealZone", "ShopRight"],
    "Fuel": ["FuelMart", "GasGo", "PetroStop", "QuickFuel", "EnergyPlus", "FuelUp", "SpeedGas"],
    "Healthcare": ["Dental Care", "MedPlus", "HealthFirst", "CarePoint", "WellLife", "MediCenter", "PharmaCare"],
    "Electronics": ["Phone Hub", "TechZone", "Computer Warehouse", "GadgetWorld", "ByteShop", "CircuitCity", "DigiStore"],
    "Grocery": ["FreshMart", "GreenBasket", "DailyGrocers", "FoodHaven", "NatureBuy", "MarketFresh", "GrocerEase"],
    "Restaurant": ["Golden Wok", "Pizza Palace", "Burger Barn", "Taco Town", "Sushi Spot", "Grill House", "Cafe Mocha"],
    "Travel": ["SkyTravel", "GoVoyage", "TripEase", "JetAway", "WanderBook", "FlyRight", "TourPlus"],
    "Entertainment": ["CinePlex", "FunZone", "GameArena", "ShowTime", "PlayPark", "StarVenue", "JoyLand"],
}

MERCHANT_CATEGORIES = list(MERCHANT_TEMPLATES.keys())

MERCHANT_COUNTRIES = ["US", "GB", "CA", "BR", "CN", "RU"]
MERCHANT_COUNTRY_WEIGHTS = [50, 15, 15, 8, 7, 5]

RISK_LEVELS = ["Low", "Medium", "High"]
RISK_LEVEL_WEIGHTS = [60, 25, 15]

ACCOUNT_TYPES = ["Checking", "Savings", "Credit"]
ACCOUNT_STATUSES = ["Active", "Suspended", "Closed"]
ACCOUNT_STATUS_WEIGHTS = [90, 5, 5]

TRANSACTION_TYPES = ["Purchase", "Online", "Transfer", "Withdrawal"]
CHANNELS = ["POS", "Mobile", "Online", "ATM"]


def _fake_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def _fake_email(name):
    parts = name.lower().split()
    sep = random.choice([".", "_", ""])
    num = random.randint(1, 999)
    return f"{parts[0]}{sep}{parts[1]}{num}@{random.choice(EMAIL_DOMAINS)}"


def _fake_phone():
    return f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"


def _fake_address():
    return f"{random.randint(1, 9999)} {random.choice(STREETS)}"


def _fake_city_state():
    return random.choice(CITIES_STATES)


def _fake_postal():
    return f"{random.randint(10000, 99999)}"


def random_date(start, end):
    delta = end - start
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=rand_seconds)


def format_ts(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Generator functions
# ---------------------------------------------------------------------------

def generate_customers(n=1000):
    print(f"Generating {n} customers...")
    customers = []
    two_years_ago = NOW - timedelta(days=730)
    seen_emails = set()

    for i in range(1, n + 1):
        cid = f"CUST{i:06d}"
        if HAS_FAKER:
            name = fake.name()
            city = fake.city()
            state = fake.state_abbr()
            address = fake.street_address()
            postal = fake.zipcode()
        else:
            name = _fake_name()
            city, state = _fake_city_state()
            address = _fake_address()
            postal = _fake_postal()

        email = _fake_email(name) if not HAS_FAKER else fake.email()
        # Ensure unique email
        while email in seen_emails:
            email = _fake_email(name) if not HAS_FAKER else fake.email()
        seen_emails.add(email)

        phone = _fake_phone() if not HAS_FAKER else fake.phone_number()
        country = "US"
        creation_date = random_date(two_years_ago, NOW)
        risk_score = random.randint(0, 100)
        is_high_risk = risk_score > 75

        customers.append({
            "customer_id": cid,
            "customer_name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal,
            "account_creation_date": format_ts(creation_date),
            "customer_risk_score": risk_score,
            "is_high_risk_customer": is_high_risk,
            "entity_type": "Customer",
            "ingestion_timestamp": format_ts(NOW),
        })

    print(f"  ✓ {n} customers generated")
    return customers


def generate_bank_accounts(customers, n=2000):
    print(f"Generating {n} bank accounts...")
    accounts = []
    customer_ids = [c["customer_id"] for c in customers]
    customer_map = {c["customer_id"]: c for c in customers}

    for i in range(1, n + 1):
        aid = f"ACCT{i:06d}"
        cid = random.choice(customer_ids)
        cust = customer_map[cid]
        acct_type = random.choice(ACCOUNT_TYPES)
        status = random.choices(ACCOUNT_STATUSES, weights=ACCOUNT_STATUS_WEIGHTS, k=1)[0]

        cust_creation = datetime.strptime(cust["account_creation_date"], "%Y-%m-%dT%H:%M:%SZ")
        opening = random_date(cust_creation, NOW)
        balance = round(random.uniform(100, 50000), 2)
        credit_limit = round(random.uniform(1000, 25000), 2) if acct_type == "Credit" else None
        daily_limit = round(random.uniform(500, 10000), 2)

        accounts.append({
            "account_id": aid,
            "customer_id": cid,
            "account_type": acct_type,
            "account_status": status,
            "opening_date": format_ts(opening),
            "current_balance": balance,
            "credit_limit": credit_limit if credit_limit else "",
            "daily_transaction_limit": daily_limit,
            "entity_type": "BankAccount",
            "ingestion_timestamp": format_ts(NOW),
        })

    print(f"  ✓ {n} bank accounts generated")
    return accounts


def generate_merchants(n=500):
    print(f"Generating {n} merchants...")
    merchants = []
    used_names = set()

    for i in range(1, n + 1):
        mid = f"MERCH{i:04d}"
        category = random.choice(MERCHANT_CATEGORIES)
        templates = MERCHANT_TEMPLATES[category]
        base_name = random.choice(templates)
        store_num = random.randint(1, 500)
        merchant_name = f"{base_name} #{store_num}"
        # Ensure unique names
        while merchant_name in used_names:
            store_num = random.randint(1, 9999)
            merchant_name = f"{base_name} #{store_num}"
        used_names.add(merchant_name)

        country = random.choices(MERCHANT_COUNTRIES, weights=MERCHANT_COUNTRY_WEIGHTS, k=1)[0]
        risk = random.choices(RISK_LEVELS, weights=RISK_LEVEL_WEIGHTS, k=1)[0]

        merchants.append({
            "merchant_id": mid,
            "merchant_name": merchant_name,
            "merchant_category": category,
            "merchant_country": country,
            "risk_level": risk,
            "entity_type": "Merchant",
            "ingestion_timestamp": format_ts(NOW),
        })

    print(f"  ✓ {n} merchants generated")
    return merchants


def generate_transactions(customers, accounts, merchants, n=10000):
    print(f"Generating {n} transactions (~5% suspicious)...")
    transactions = []
    thirty_days_ago = NOW - timedelta(days=30)

    customer_map = {c["customer_id"]: c for c in customers}
    account_list = [(a["account_id"], a["customer_id"]) for a in accounts
                    if a["account_status"] == "Active"]
    if not account_list:
        account_list = [(a["account_id"], a["customer_id"]) for a in accounts]

    suspicious_count = 0
    target_suspicious = int(n * 0.05)

    for i in range(1, n + 1):
        tid = f"TXN{i:010d}"
        acct_id, cust_id = random.choice(account_list)
        cust = customer_map[cust_id]
        merch = random.choice(merchants)

        is_suspicious = suspicious_count < target_suspicious and random.random() < 0.055

        if is_suspicious:
            suspicious_count += 1
            # Suspicious: high amount, cross-border, unusual hour (1-5 AM)
            amount = round(random.uniform(2000, 10000), 2)
            # Pick a foreign merchant country different from customer country
            foreign_countries = [c for c in MERCHANT_COUNTRIES if c != cust["country"]]
            cross_border_merch = [m for m in merchants if m["merchant_country"] in foreign_countries]
            if cross_border_merch:
                merch = random.choice(cross_border_merch)
            ts = random_date(thirty_days_ago, NOW)
            # Force unusual hour (1-5 AM)
            ts = ts.replace(hour=random.randint(1, 4), minute=random.randint(0, 59))
            channel = random.choice(["Online", "Mobile"])
            card_present = False
            txn_type = random.choice(["Online", "Transfer"])
        else:
            # Normal transaction
            if random.random() < 0.05:
                amount = round(random.uniform(2000, 10000), 2)
            else:
                amount = round(random.uniform(5, 2000), 2)
            ts = random_date(thirty_days_ago, NOW)
            channel = random.choice(CHANNELS)
            if channel == "POS":
                card_present = True
            elif channel == "Online":
                card_present = False
            else:
                card_present = random.choice([True, False])
            txn_type = random.choice(TRANSACTION_TYPES)

        transactions.append({
            "transaction_id": tid,
            "timestamp": format_ts(ts),
            "account_id": acct_id,
            "customer_id": cust_id,
            "merchant_id": merch["merchant_id"],
            "merchant_name": merch["merchant_name"],
            "merchant_category": merch["merchant_category"],
            "amount": amount,
            "currency": "USD",
            "transaction_type": txn_type,
            "channel": channel,
            "card_present": card_present,
            "merchant_country": merch["merchant_country"],
            "customer_city": cust["city"],
            "customer_country": cust["country"],
            "customer_risk_score": cust["customer_risk_score"],
            "merchant_risk_level": merch["risk_level"],
            "entity_type": "Transaction",
            "ingestion_timestamp": format_ts(NOW),
        })

    print(f"  ✓ {n} transactions generated ({suspicious_count} suspicious)")
    return transactions


def write_csv(filename, rows):
    if not rows:
        return
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  → Saved {filepath} ({len(rows)} rows, {size_kb:.1f} KB)")


def main():
    print("=" * 60)
    print("  Fraud Detection Sample Data Generator")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Timestamp: {format_ts(NOW)}")
    print(f"Random seed: 42")
    print(f"Faker available: {HAS_FAKER}")
    print("-" * 60)

    customers = generate_customers(1000)
    accounts = generate_bank_accounts(customers, 2000)
    merchants = generate_merchants(500)
    transactions = generate_transactions(customers, accounts, merchants, 10000)

    print("-" * 60)
    print("Writing CSV files...")
    write_csv("customers.csv", customers)
    write_csv("bankaccounts.csv", accounts)
    write_csv("merchants.csv", merchants)
    write_csv("transactions.csv", transactions)

    print("-" * 60)
    print("Summary:")
    print(f"  Customers:    {len(customers):>6,}")
    print(f"  Bank Accounts:{len(accounts):>6,}")
    print(f"  Merchants:    {len(merchants):>6,}")
    print(f"  Transactions: {len(transactions):>6,}")

    high_risk = sum(1 for c in customers if c["is_high_risk_customer"])
    cross_border = sum(1 for t in transactions if t["merchant_country"] != t["customer_country"])
    high_amount = sum(1 for t in transactions if t["amount"] > 2000)
    print(f"\n  High-risk customers: {high_risk}")
    print(f"  Cross-border txns:   {cross_border}")
    print(f"  High-amount txns:    {high_amount}")
    print("=" * 60)
    print("Done! Data generation complete.")


if __name__ == "__main__":
    main()
