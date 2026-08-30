import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("MONDAY_API_TOKEN")
DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_ORDERS_BOARD_ID = os.getenv("WORK_ORDERS_BOARD_ID")

url = "https://api.monday.com/v2"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

query = """
query ($board_id: [ID!]) {
    boards(ids: $board_id) {
        id
        name
    }
}
"""

def check_board(board_id):
    response = requests.post(
        url,
        json={
            "query": query,
            "variables": {
                "board_id": board_id
            }
        },
        headers=headers
    )

    print(response.status_code)
    print(response.json())


print("Checking Deals board...")
check_board(DEALS_BOARD_ID)

print("\nChecking Work Orders board...")
check_board(WORK_ORDERS_BOARD_ID)