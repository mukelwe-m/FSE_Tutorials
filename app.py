from loguru import logger

from transactions import Transaction, Category, calculate_financial_summary
from database import get_session
from sqlalchemy import select


def main():
    logger.add("logs/app.log", rotation="1 MB")
    # Initialize database and create tables
    # Get a session
    session = get_session()

    try:
        # Ensure transaction table exists by querying it
        session.query(Transaction).first()

        # Query all transactions from the database
        all_transactions = session.query(Transaction).all()

        # Calculate and display summary
        summary = calculate_financial_summary(all_transactions)
        print("Financial Summary:")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    except Exception as e:
        logger.error(
            f"You may need to seed the database first, run 'python seed.py' and try again.\n\n"
        )
        raise e

    finally:
        session.close()
        # TODO: Once you have added the Entertainment category and sample  expenses, uncomment the lines below to display them!
        display_transactions_by_category("Job")
        display_transactions_by_category("Entertainment")


# TODO: Add the entertainment category, if it does not already exist
# NOTE: This means checking if a category with that name exists first == DONE!
def add_entertainment_category():
    session = get_session()
    try:
        # Check if the Entertainment category already exists
        entertainment_category = (
            session.query(Category).filter_by(name="Entertainment").first()
        )
        if not entertainment_category:
            # If it doesn't exist, create it
            entertainment_category = Category(name="Entertainment")
            session.add(entertainment_category)
            session.commit()  # Commit to get the ID assigned
            logger.info("Added 'Entertainment' category to the database.")
        else:
            logger.info("'Entertainment' category already exists in the database.")
    finally:
        session.close()


# TODO: Add sample entertainment expenses == DONE!
# NOTE: Fetch the Entertainment category first, then add two sample expenses linked to that category
def add_entertainment_expenses():
    session = get_session()
    try:
        # Fetch the Entertainment category
        entertainment_category = (
            session.query(Category).filter_by(name="Entertainment").first()
        )
        if not entertainment_category:
            logger.error(
                "Entertainment category does not exist. Please add it first using add_entertainment_category()."
            )
            return

        # Create sample expenses
        expense1 = Transaction(
            date="2026-03-01",
            description="Concert Tickets",
            amount=-600.00,
            category_ref=entertainment_category,
        )
        expense2 = Transaction(
            date="2026-02-15",
            description="Petrol",
            amount=-300.00,
            category_ref=entertainment_category,
        )

        # Add expenses to the session and commit
        session.add_all([expense1, expense2])
        session.commit()
        logger.info("Added sample entertainment expenses to the database.")
    finally:
        session.close()


# TODO: Display all transactions for a given category name
def display_transactions_by_category(category_name: str):
    session = get_session()
    try:
        # Fetch the category by name
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            logger.error(f"Category '{category_name}' does not exist.")
            return

        # Fetch transactions for the category
        transactions = (
            session.query(Transaction)
            .filter(Transaction.category_id == category.id)
            .all()
        )

        # Display transactions
        print(f"\nTransactions in category '{category_name}':")
        for transaction in transactions:
            print(
                f"Date: {transaction.date}, Description: {transaction.description}, Amount: {transaction.amount}"
            )
    except Exception as e:
        logger.error(
            f"Error displaying transactions for category '{category_name}': {e}"
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
