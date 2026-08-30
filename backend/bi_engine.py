import pandas as pd
import re


DEAL_COLUMNS = {
    "name": "deal_name",
    "text_mm6qz38c": "deal_value",
    "text_mm6q60ad": "expected_close_date",
    "text_mm6qw4z7": "stage",
    "text_mm6qy2yf": "deal_status",
    "text_mm6qppf4": "sector",
    "text_mm6qd514": "created_date",
    "text_mm6q4nnk": "client_code",
    "text_mm6qn319": "owner",
    "text_mm6q19cq": "product",
}


WORK_ORDER_COLUMNS = {
    "name": "work_order_name",
    "color_mm6qcdb": "work_order_status",
    "date_mm6qxrzk": "due_date",
    "date_mm6q7wvx": "work_order_date",
    "numeric_mm6q250f": "estimated_hours",
    "text_mm6qafr0": "sector",
    "text_mm6q23vy": "execution_status",
    "text_mm6qq0nz": "amount_excl_gst",
    "text_mm6qp8tv": "billed_value_excl_gst",
    "text_mm6qvzs8": "collected_amount",
    "text_mm6qycnp": "amount_receivable",
    "text_mm6q5hb8": "billing_status",
    "text_mm6q14c9": "collection_status",
}


def normalize_columns(df, mapping):
    result = pd.DataFrame()

    for old_name, new_name in mapping.items():
        if old_name in df.columns:
            result[new_name] = df[old_name]
        else:
            result[new_name] = ""

    return result


def clean_text(value):
    if value is None:
        return ""

    text = str(value).strip()

    if text.lower() in ["nan", "none", "null", "n/a", "na", "-"]:
        return ""

    return re.sub(r"\s+", " ", text)


def clean_number(value):
    if value is None:
        return 0.0

    text = str(value).strip()

    if not text:
        return 0.0

    text = re.sub(r"[₹,$]", "", text)
    text = text.replace(",", "")
    text = re.sub(r"[^0-9.\-]", "", text)

    try:
        return float(text)
    except (ValueError, TypeError):
        return 0.0


def clean_percentage(value):
    if value is None:
        return 0.0

    text = str(value).strip().replace("%", "")

    if not text:
        return 0.0

    try:
        number = float(text)

        if number > 1:
            number = number / 100

        return number
    except (ValueError, TypeError):
        return 0.0


def clean_date(value):
    if value is None or str(value).strip() == "":
        return pd.NaT

    text = str(value).strip()

    # Remove timezone text from Monday's date format
    text = re.sub(r"\sGMT[+-]\d{4}.*$", "", text)

    return pd.to_datetime(text, errors="coerce")


def prepare_deals(df):
    deals = normalize_columns(df, DEAL_COLUMNS)

    deals["deal_value"] = deals["deal_value"].apply(clean_number)

    deals["sector"] = deals["sector"].apply(clean_text).str.title()

    deals["stage"] = deals["stage"].apply(clean_text)

    deals["deal_status"] = deals["deal_status"].apply(clean_text)

    deals["expected_close_date"] = deals[
        "expected_close_date"
    ].apply(clean_date)

    deals["created_date"] = deals[
        "created_date"
    ].apply(clean_date)

    return deals


def prepare_work_orders(df):
    orders = normalize_columns(df, WORK_ORDER_COLUMNS)

    numeric_fields = [
        "estimated_hours",
        "amount_excl_gst",
        "billed_value_excl_gst",
        "collected_amount",
        "amount_receivable",
    ]

    for field in numeric_fields:
        orders[field] = orders[field].apply(clean_number)

    orders["sector"] = (
        orders["sector"]
        .apply(clean_text)
        .str.title()
    )

    orders["execution_status"] = (
        orders["execution_status"]
        .apply(clean_text)
    )

    orders["due_date"] = orders[
        "due_date"
    ].apply(clean_date)

    orders["work_order_date"] = orders[
        "work_order_date"
    ].apply(clean_date)

    return orders


def pipeline_summary(deals):
    total_pipeline = deals["deal_value"].sum()

    return {
        "total_deals": len(deals),
        "total_pipeline": round(float(total_pipeline), 2),
    }


def pipeline_by_sector(deals):
    result = (
        deals[deals["sector"] != ""]
        .groupby("sector")["deal_value"]
        .agg(["count", "sum"])
        .reset_index()
        .sort_values("sum", ascending=False)
    )

    result.columns = [
        "sector",
        "deal_count",
        "pipeline_value"
    ]

    return result


def pipeline_by_stage(deals):
    result = (
        deals[deals["stage"] != ""]
        .groupby("stage")["deal_value"]
        .agg(["count", "sum"])
        .reset_index()
        .sort_values("sum", ascending=False)
    )

    result.columns = [
        "stage",
        "deal_count",
        "pipeline_value"
    ]

    return result


def work_order_summary(orders):
    total = len(orders)

    completed = orders[
        orders["execution_status"]
        .str.lower()
        .str.contains(
            "complete|executed",
            na=False
        )
    ]

    completion_rate = (
        len(completed) / total * 100
        if total > 0
        else 0
    )

    return {
        "total_work_orders": total,
        "completed_work_orders": len(completed),
        "completion_rate": round(completion_rate, 2),
        "total_billed": round(
            orders["billed_value_excl_gst"].sum(), 2
        ),
        "total_collected": round(
            orders["collected_amount"].sum(), 2
        ),
        "total_receivable": round(
            orders["amount_receivable"].sum(), 2
        ),
    }