import pytest
from decimal import Decimal
from transactions import Transaction, format_currency, calculate_total_expenses, calculate_total_income, calculate_balance, check_financial_health

'''
all sample_transactions does is create a list of Transaction objects that can be used in multiple tests. 
But I dont want them to be defined in each test function, so I use a fixture to create them once and then pass them to any test that needs them.
With pytest fixture I am telling pytest that if you want to run a test you have to use these sample transactions, and pytest will automatically create them for you before running the test.
This way I can reuse the same set of transactions across multiple tests without having to duplicate the code.
We access fixtures like args.
'''
@pytest.fixture
def sample_transactions():
    return [
        Transaction('2024-01-01', 'Salary', Decimal('10000.00'), 'Income'),
        Transaction('2024-01-02', 'Groceries', Decimal('-500.00'), 'Food'),
        Transaction('2024-01-03', 'Rent', Decimal('-4000.00'), 'Housing'),
        Transaction('2024-01-04', 'Freelance', Decimal('1500.00'), 'Income'),
        Transaction('2024-01-05', 'Dinner', Decimal('-250.50'), 'Food'),
    ]


@pytest.fixture
def income_only_transactions():
    return [
        Transaction('2024-01-01', 'Salary', Decimal('3000.00'), 'Income'),
        Transaction('2024-01-02', 'Bonus', Decimal('500.00'), 'Income'),
    ]

@pytest.fixture
def expenses_only_transactions():
    return [
        Transaction('2024-01-01', 'Groceries', Decimal('-200.00'), 'Food'),
        Transaction('2024-01-02', 'Rent', Decimal('-800.00'), 'Housing'),
    ]

def test_transaction_creation():
    t = Transaction('2024-01-01', 'Test', '100.00', 'Test Category')
    assert t.date == '2024-01-01'
    assert t.description == 'Test'
    assert t.amount == Decimal('100.00')
    assert t.category == 'Test Category'

def test_invalid_amount():
    with pytest.raises(ValueError):
        Transaction('2024-01-01', 'Invalid', 'abc', 'Error')

def test_format_currency():
    assert format_currency(Decimal('123.456')) == 'R 123.46'
    assert format_currency(Decimal('-50.00')) == 'R -50.00'

def test_calculate_total_expenses(sample_transactions):
    assert calculate_total_expenses(sample_transactions) == Decimal('-4750.50')

def test_calculate_total_income(sample_transactions):
    assert calculate_total_income(sample_transactions) == Decimal('11500.00')

def test_calculate_balance(sample_transactions):
    assert calculate_balance(sample_transactions) == Decimal('6749.50')

#NOTE This is an example of a test, you should add more tests to cover different scenarios
def test_empty_transactions():
    empty_list = []
    assert calculate_total_expenses(empty_list) == Decimal('0')
    assert calculate_total_income(empty_list) == Decimal('0')
    assert calculate_balance(empty_list) == Decimal('0')
    assert check_financial_health(empty_list) == "No transactions recorded!"  # Since income is 0

#TODO Complete this test
def test_only_expenses(expenses_only_transactions):
    # because if expenses only, income should be zero.
    assert calculate_total_income(expenses_only_transactions) == Decimal('0')
    # Expenses should sum to -1000.00 (-200 + -800)
    assert calculate_total_expenses(expenses_only_transactions) == Decimal('-1000.00')
    #Balance should equal expenses (negative)
    assert calculate_balance(expenses_only_transactions) == Decimal('-1000.00')
    assert check_financial_health(expenses_only_transactions) == "Overspending"  # Since we have expenses but no income, we are overspending.


#TODO Complete this test
def test_only_income(income_only_transactions):
    # Expenses should be zero
    assert calculate_total_expenses(income_only_transactions) == Decimal(0)
    # Income should sum to 3500.00 (3000 + 500)
    assert calculate_total_income(income_only_transactions) == Decimal('3500.00')
    # Balance should equal income (positive)
    assert calculate_balance(income_only_transactions) == Decimal('3500.00')
    # Financial health should show "Saving well" (handled by our try-except!)
    assert check_financial_health(income_only_transactions) == "Saving well"

#TODO Complete this test
def test_mixed_transactions(sample_transactions):
    # Income is 11,500 (10,000 + 1,500)
    assert calculate_total_income(sample_transactions) == Decimal('11500.00')
    # Expenses is 4,750.50 (500 + 4,000 + 250.50)
    assert calculate_total_expenses(sample_transactions) == Decimal('-4750.50')
    # Balance is 6,749.50 (11,500 - 4,750.50)
    assert calculate_balance(sample_transactions) == Decimal('6749.50')
    # Financial health should be "Good" since income > expenses
    assert check_financial_health(sample_transactions) == "Saving well"