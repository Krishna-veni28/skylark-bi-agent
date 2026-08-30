from monday_client import get_deals

deals = get_deals()

items = deals["items_page"]["items"]

print("Total items:", len(items))

print("\n========== FIRST DEAL ==========")

first_item = items[0]

print("ID:", first_item["id"])
print("Name:", first_item["name"])

print("\n========== COLUMN VALUES ==========")

for column in first_item["column_values"]:
    print("\nColumn ID:", column["id"])
    print("Text:", repr(column.get("text")))
    print("Value:", repr(column.get("value")))