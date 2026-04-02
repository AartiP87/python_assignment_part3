# ============================================
# Product Explorer & Error Logger
# ============================================

import requests
from datetime import datetime

# --------------------------------
# Task 1 — File Write & Read
# --------------------------------

# writing notes
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# write mode
with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")

print("File written successfully.")

# append mode
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help reuse code.\n")
    f.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")

# reading file
print("\nReading file:\n")

lines = []
with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, start=1):
    print(f"{i}. {line.strip()}")

print("Total lines:", len(lines))

# keyword search
key = input("\nEnter keyword to search: ").lower()

found = False
for line in lines:
    if key in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# --------------------------------
# Task 2 — API Integration
# --------------------------------

BASE_URL = "https://dummyjson.com/products"

def log_error(context, message):
    with open("error_log.txt", "a") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] ERROR in {context}: {message}\n")

# fetch products
try:
    res = requests.get(f"{BASE_URL}?limit=20", timeout=5)
    data = res.json()

    print("\nProduct List:")
    print("ID | Title | Category | Price | Rating")

    products = data["products"]

    for p in products:
        print(p["id"], "|", p["title"], "|", p["category"], "|", p["price"], "|", p["rating"])

except requests.exceptions.ConnectionError:
    print("Connection failed.")
    log_error("fetch_products", "ConnectionError")
except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("fetch_products", "Timeout")
except Exception as e:
    print("Error:", e)
    log_error("fetch_products", str(e))


# filter + sort
filtered = []

for p in products:
    if p["rating"] >= 4.5:
        filtered.append(p)

filtered.sort(key=lambda x: x["price"], reverse=True)

print("\nFiltered Products:")
for p in filtered:
    print(p["title"], p["price"], p["rating"])


# category search
try:
    res = requests.get(f"{BASE_URL}/category/laptops", timeout=5)
    laptops = res.json()["products"]

    print("\nLaptops:")
    for l in laptops:
        print(l["title"], "-", l["price"])

except Exception as e:
    print("Error fetching laptops")
    log_error("laptop_fetch", str(e))


# POST request
try:
    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }

    res = requests.post(f"{BASE_URL}/add", json=new_product, timeout=5)
    print("\nPOST Response:")
    print(res.json())

except Exception as e:
    print("POST failed")
    log_error("post_product", str(e))


# --------------------------------
# Task 3 — Exception Handling
# --------------------------------

# safe divide
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nSafe Divide Tests:")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# safe file reader
def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

print("\nReading existing file:")
print(read_file_safe("python_notes.txt"))

print("\nReading missing file:")
read_file_safe("ghost_file.txt")


# input validation loop
while True:
    user_input = input("\nEnter product ID (1–100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("Out of range")
        continue

    try:
        res = requests.get(f"{BASE_URL}/{pid}", timeout=5)

        if res.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", f"404 for ID {pid}")
        else:
            data = res.json()
            print(data["title"], "-", data["price"])

    except Exception as e:
        print("Error fetching product")
        log_error("lookup_product", str(e))


# --------------------------------
# Task 4 — Logging
# --------------------------------

# force connection error
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error("forced_connection", str(e))

# force 404 log
try:
    res = requests.get(f"{BASE_URL}/999", timeout=5)
    if res.status_code != 200:
        log_error("forced_404", "404 Not Found for product ID 999")
except Exception as e:
    log_error("forced_404", str(e))


# print log file
print("\nError Log Contents:\n")
try:
    with open("error_log.txt", "r") as f:
        print(f.read())
except:
    print("No log file found")
