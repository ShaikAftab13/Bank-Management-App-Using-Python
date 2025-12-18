import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"

    def __init__(self):
        if Path(self.database).exists():
            with open(self.database, "r") as f:
                try:
                    self.data = json.load(f)
                except:
                    self.data = []
        else:
            self.data = []

    def save(self):
        with open(self.database, "w") as f:
            json.dump(self.data, f, indent=4)

    def generate_account_number(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # ---------------- CREATE ACCOUNT ----------------
    def create_account(self, name, age, email, pin):
        if age < 18:
            return "❌ Age must be 18+"
        if len(str(pin)) != 4:
            return "❌ PIN must be exactly 4 digits"
        if len(name) < 3:
            return "❌ Name too short"
        if "@" not in email or "." not in email:
            return "❌ Invalid email"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": self.generate_account_number(),
            "balance": 0,
            "transactions": []
        }

        self.data.append(account)
        self.save()
        return f"✅ Account created successfully!\nAccount No: {account['account_number']}"

    # ---------------- AUTH ----------------
    def get_user(self, acc, pin):
        return next((u for u in self.data if u["account_number"] == acc and u["pin"] == pin), None)

    # ---------------- DEPOSIT ----------------
    def deposit(self, acc, pin, amount):
        user = self.get_user(acc, pin)
        if not user:
            return "❌ Invalid account or PIN"
        if amount <= 0:
            return "❌ Invalid amount"

        user["balance"] += amount
        user["transactions"].append({"type": "Deposit", "amount": amount})
        self.save()
        return f"✅ ₹{amount} deposited\nBalance: ₹{user['balance']}"

    # ---------------- WITHDRAW ----------------
    def withdraw(self, acc, pin, amount):
        user = self.get_user(acc, pin)
        if not user:
            return "❌ Invalid account or PIN"
        if amount <= 0:
            return "❌ Invalid amount"
        if user["balance"] < amount:
            return "❌ Insufficient balance"

        user["balance"] -= amount
        user["transactions"].append({"type": "Withdraw", "amount": amount})
        self.save()
        return f"✅ ₹{amount} withdrawn\nBalance: ₹{user['balance']}"

    # ---------------- UPDATE ----------------
    def update(self, acc, pin, name=None, email=None, new_pin=None):
        user = self.get_user(acc, pin)
        if not user:
            return "❌ Invalid account or PIN"

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if new_pin:
            user["pin"] = new_pin

        self.save()
        return "✅ Details updated successfully"

    # ---------------- DELETE ----------------
    def delete(self, acc, pin):
        user = self.get_user(acc, pin)
        if not user:
            return "❌ Invalid account or PIN"

        self.data.remove(user)
        self.save()
        return "✅ Account deleted successfully"
