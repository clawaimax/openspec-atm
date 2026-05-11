"""
ATM terminal application entry point.

This file is intentionally simple — the focus of this project is the
OpenSpec demonstration, not the terminal UI.  Run the app with:

    python -m atm.main

The tests in tests/ are the recommended way to exercise the domain logic.
"""

from .account import Account
from .atm import ATM, ATMError


def _seed_accounts() -> ATM:
    atm = ATM(cash_available=10_000.00)
    atm.load_account(Account("1001", "Alice Smith", "1234", 2_500.00))
    atm.load_account(Account("1002", "Bob Jones", "5678", 800.00))
    return atm


def _menu() -> str:
    print("\n--- ATM Menu ---")
    print("1. Check balance")
    print("2. Withdraw cash")
    print("3. Transfer funds")
    print("4. Deposit cash")
    print("5. Deposit cheque")
    print("6. Exit")
    return input("Choose an option: ").strip()


def run() -> None:
    print("Welcome to the OpenSpec ATM Demo")
    atm = _seed_accounts()

    account_number = input("Enter account number: ").strip()
    try:
        atm.insert_card(account_number)
    except ATMError as exc:
        print(f"Error: {exc}")
        return

    for _ in range(atm.max_pin_attempts):
        pin = input("Enter PIN: ").strip()
        try:
            ok = atm.enter_pin(pin)
        except ATMError as exc:
            print(f"Error: {exc}")
            return
        if ok:
            print("PIN accepted.")
            break
        print("Incorrect PIN.")
    else:
        print(f"Account locked after {atm.max_pin_attempts} failed attempts.")
        return

    while True:
        choice = _menu()
        if choice == "1":
            try:
                balance = atm.check_balance()
                print(f"Available balance: ${balance:,.2f}")
            except ATMError as exc:
                print(f"Error: {exc}")
        elif choice == "2":
            try:
                amount = float(input("Enter amount to withdraw: $").strip())
                new_balance = atm.withdraw(amount)
                print(f"Dispensing ${amount:,.2f}. New balance: ${new_balance:,.2f}")
            except (ATMError, ValueError) as exc:
                print(f"Error: {exc}")
        elif choice == "3":
            try:
                dest = input("Enter destination account number: ").strip()
                amount = float(input("Enter amount to transfer: $").strip())
                new_balance = atm.transfer(amount, dest)
                print(f"Transferred ${amount:,.2f} to {dest}. New balance: ${new_balance:,.2f}")
            except (ATMError, ValueError) as exc:
                print(f"Error: {exc}")
        elif choice == "4":
            try:
                amount = float(input("Enter cash amount to deposit: $").strip())
                new_balance = atm.deposit_cash(amount)
                print(f"Deposited ${amount:,.2f}. New balance: ${new_balance:,.2f}")
            except (ATMError, ValueError) as exc:
                print(f"Error: {exc}")
        elif choice == "5":
            try:
                amount = float(input("Enter cheque amount to deposit: $").strip())
                new_balance = atm.deposit_check(amount)
                print(f"Cheque of ${amount:,.2f} deposited (pending). New balance: ${new_balance:,.2f}")
            except (ATMError, ValueError) as exc:
                print(f"Error: {exc}")
        elif choice == "6":
            print("Thank you for using the ATM. Goodbye.")
            atm.end_session()
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run()
