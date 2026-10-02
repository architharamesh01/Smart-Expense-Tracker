import streamlit as st
import json
import os

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰"
)

# ---------------- SAVE FILE ----------------

file_name = "expenses.json"


# Load saved expenses
if os.path.exists(file_name):

    with open(file_name, "r") as file:
        expenses = json.load(file)

else:

    expenses = []


# ---------------- TITLE ----------------

st.title("💰 Smart Expense Tracker")
st.write("Track your money easily.")

st.divider()


# ---------------- BUDGET ----------------

st.header("🎯 Monthly Budget")

budget = st.number_input(
    "Enter your monthly budget (₹)",
    min_value=0,
    value=10000
)


# ---------------- ADD EXPENSE ----------------

st.header("➕ Add Expense")

amount = st.number_input(
    "Amount (₹)",
    min_value=0
)

category = st.selectbox(
    "Category",
    [
        "Food",
        "Shopping",
        "Transport",
        "Education",
        "Entertainment",
        "Bills",
        "Other"
    ]
)

date = st.date_input("Date")

payment = st.selectbox(
    "Payment Method",
    [
        "Cash",
        "Debit Card",
        "Credit Card",
        "Bank Transfer"
    ]
)


# Add button
if st.button("Add Expense"):

    if amount > 0:

        new_expense = {
            "amount": amount,
            "category": category,
            "date": str(date),
            "payment": payment
        }

        expenses.append(new_expense)

        # Save expenses
        with open(file_name, "w") as file:
            json.dump(expenses, file)

        st.success("Expense added! ✅")

        st.rerun()

    else:

        st.warning("Please enter an amount.")


# ---------------- TOTAL ----------------

total = 0

for expense in expenses:

    total = total + expense["amount"]


remaining = budget - total


# ---------------- DASHBOARD ----------------

st.divider()

st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "💰 Total Spent",
        f"₹{total}"
    )

with col2:

    st.metric(
        "🎯 Budget",
        f"₹{budget}"
    )

with col3:

    st.metric(
        "💵 Remaining",
        f"₹{remaining}"
    )


# ---------------- EXPENSE LIST ----------------

st.divider()

st.header("📋 My Expenses")


if len(expenses) == 0:

    st.info("No expenses added yet.")

else:

    for i, expense in enumerate(expenses):

        st.write(
            f"**₹{expense['amount']}**  |  "
            f"{expense['category']}  |  "
            f"{expense['date']}  |  "
            f"{expense['payment']}"
        )

        # Delete button
        if st.button("🗑️ Delete", key=i):

            expenses.pop(i)

            with open(file_name, "w") as file:
                json.dump(expenses, file)

            st.rerun()


# ---------------- BUDGET WARNING ----------------

if total > budget and budget > 0:

    st.error("⚠️ You have exceeded your monthly budget!")

elif budget > 0 and total >= budget * 0.8:

    st.warning("⚠️ You have used more than 80% of your budget.")

else:

    st.success("✅ You are within your budget.")