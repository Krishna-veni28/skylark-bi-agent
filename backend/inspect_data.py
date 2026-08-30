from monday_client import get_deals, get_work_orders
from data_cleaner import clean_board


def inspect_board(name, board_data):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("\nColumns:")
    for column in board_data["columns"]:
        print(f"- {column['id']} | {column['title']} | {column['type']}")

    df = clean_board(board_data)

    print("\nData shape:")
    print(df.shape)

    print("\nCleaned column names:")
    for column in df.columns:
        print("-", column)

    print("\nFirst 3 records:")
    print(df.head(3).to_string(index=False))


print("Loading Deals...")
deals = get_deals()
inspect_board("DEALS", deals)

print("\n\nLoading Work Orders...")
work_orders = get_work_orders()
inspect_board("WORK ORDERS", work_orders)