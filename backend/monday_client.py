import os
import requests
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"

TOKEN = os.getenv("MONDAY_API_TOKEN")
DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_ORDERS_BOARD_ID = os.getenv("WORK_ORDERS_BOARD_ID")


def get_board_items(board_id):
    query = """
    query ($board_id: [ID!]) {
        boards(ids: $board_id) {
            id
            name
            columns {
                id
                title
                type
            }
            items_page(limit: 500) {
                items {
                    id
                    name
                    column_values {
                        id
                        text
                        value
                    }
                }
            }
        }
    }
    """

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_API_URL,
        json={
            "query": query,
            "variables": {
                "board_id": str(board_id)
            }
        },
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(
            f"Monday API error: {response.status_code} {response.text}"
        )

    data = response.json()

    if "errors" in data:
        raise Exception(f"Monday API error: {data['errors']}")

    boards = data.get("data", {}).get("boards", [])

    if not boards:
        raise Exception(f"Board {board_id} was not found.")

    return boards[0]


def get_deals():
    return get_board_items(DEALS_BOARD_ID)


def get_work_orders():
    return get_board_items(WORK_ORDERS_BOARD_ID)


if __name__ == "__main__":
    print("Fetching Deals...")
    deals = get_deals()

    print("Board:", deals["name"])
    print("Number of items:", len(deals["items_page"]["items"]))

    print("\nFetching Work Orders...")
    work_orders = get_work_orders()

    print("Board:", work_orders["name"])
    print("Number of items:", len(work_orders["items_page"]["items"]))