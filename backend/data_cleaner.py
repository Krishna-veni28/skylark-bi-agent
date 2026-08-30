import pandas as pd
import re


def clean_text(value):
    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() in ["nan", "none", "null", "n/a", "na", "-"]:
        return ""

    value = re.sub(r"\s+", " ", value)

    return value


def clean_date(value):
    if not value:
        return None

    date = pd.to_datetime(value, errors="coerce")

    if pd.isna(date):
        return None

    return date.strftime("%Y-%m-%d")


def clean_items(board_data):
    cleaned = []

    for item in board_data["items_page"]["items"]:

        record = {
            "id": item["id"],
            "name": clean_text(item["name"])
        }

        for column in item["column_values"]:
            column_id = column["id"]

            # Normally use the readable text value
            value = column.get("text", "")

            # Number/date/status values may have empty text.
            # In that case, use the raw JSON value.
            if not value and column.get("value"):
                value = column["value"]

            record[column_id] = clean_text(value)

        cleaned.append(record)

    return pd.DataFrame(cleaned)


def clean_board(board_data):
    df = clean_items(board_data)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Normalize column names
    df.columns = [
        str(col).strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    return df