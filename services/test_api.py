import requests
import json

base_url = "http://localhost:8000"

def test_api():
    # Test 1: Categories
    r = requests.get(f"{base_url}/categories/2024-10")
    print("1. Categories:", r.status_code, r.json())

    # Test 2: Add expense trigger alert
    expense_data = {"month": "2024-10", "category": "Food", "amount": 450}
    r = requests.post(f"{base_url}/expenses/", json=expense_data)
    print("2. Add expense:", r.status_code, r.json())

    # Test 3: Categories updated
    r = requests.get(f"{base_url}/categories/2024-10")
    print("3. Categories updated:", r.status_code, r.json())

    # Test 4: Threshold
    r = requests.put(f"{base_url}/config/threshold", json={"threshold": 75})
    print("4. Threshold:", r.status_code, r.json())

if __name__ == "__main__":
    test_api()
