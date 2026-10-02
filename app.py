import streamlit as st
import json
import os

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="centered"
)

# ---------------- FILE ----------------

file_name = "expenses.json"

# ---------------- LOAD SAVED DATA ----------------

if os.path.exists(file_name):

    try:
        with open(file_name, "r") as file:
            data = json.load(file)

        # New format
        if isinstance(data, dict):
            expenses = data.get("expenses", [])
            saved_budget = data.get("budget", 10000)

        # Old format (if your existing file only contains expenses)
        else:
            expenses = data
            saved_budget = 10000

    except:
        expenses = []
        saved_budget = 10000

else:

    expenses = []
    saved_budget = 10000


# ---------------- TITLE ----------------

st.title("💰 Smart Expense Tracker")
st.write("Track your money easily.")

st.divider()


# ---------------- BUDGET ----------------

st.header("🎯 Monthly Budget")

budget = st.number_input(
    "Enter your monthly budget (₹)",
    min_value=0,
    value=int(saved_budget),
    step=100
)


# ---------------- SAVE DATA FUNCTION ----------------

def save_data():
    data = {
        "budget": budget,
        "expenses": expenses
    }

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- SAVE BUDGET ----------------

if budget != saved_budget:

    data = {
        "budget": budget,
        "expenses": expenses
    }

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


# ---------------- ADD EXPENSE ----------------

st.header("➕ Add Expense")

amount = st.number_input(
    "Amount (₹)",
    min_value=0,
    step=10
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


# ---------------- ADD BUTTON ----------------

if st.button("Add Expense", use_container_width=True):

    if amount > 0:

        new_expense = {
            "amount": amount,
            "category": category,
            "date": str(date),
            "payment": payment
        }

        expenses.append(new_expense)

        save_data()

        st.success("Expense added! ✅")

        st.rerun()

    else:

        st.warning("Please enter an amount.")


# ---------------- CALCULATE TOTAL ----------------

total = 0

for expense in expenses:
    total += expense["amount"]


remaining = budget - total


# ---------------- DASHBOARD ----------------

st.divider()

st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "💰 Total Spent",
        f"₹{total:,.0f}"
    )

with col2:

    st.metric(
        "🎯 Budget",
        f"₹{budget:,.0f}"
    )

with col3:

    st.metric(
        "💵 Remaining",
        f"₹{remaining:,.0f}"
    )


# ---------------- EXPENSE LIST ----------------

st.divider()

st.header("📋 My Expenses")


if len(expenses) == 0:

    st.info("No expenses added yet.")

else:

    for i, expense in enumerate(expenses):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write(
                f"**₹{expense['amount']:,.0f}**  |  "
                f"{expense['category']}  |  "
                f"{expense['date']}  |  "
                f"{expense['payment']}"
            )

        with col2:

            if st.button("🗑️", key=f"delete_{i}"):

                expenses.pop(i)

                save_data()

                st.rerun()


# ---------------- BUDGET WARNING ----------------

st.divider()

if budget > 0:

    if total > budget:

        st.error(
            "⚠️ You have exceeded your monthly budget!"
        )

    elif total >= budget * 0.8:

        st.warning(
            "⚠️ You have used more than 80% of your budget."
        )

    else:

        st.success(
            "✅ You are within your budget."
        )
