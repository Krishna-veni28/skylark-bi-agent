from monday_client import get_deals, get_work_orders
from data_cleaner import clean_board
from bi_engine import (
    prepare_deals,
    prepare_work_orders,
    pipeline_summary,
    pipeline_by_sector,
    pipeline_by_stage,
    work_order_summary,
)


def load_data():
    deals_raw = get_deals()
    orders_raw = get_work_orders()

    deals_df = clean_board(deals_raw)
    orders_df = clean_board(orders_raw)

    deals = prepare_deals(deals_df)
    orders = prepare_work_orders(orders_df)

    return deals, orders


def answer_query(question):
    question = question.lower().strip()

    deals, orders = load_data()

    # -------------------------------------------------
    # SECTOR ANALYSIS
    # -------------------------------------------------

    # Most deals = highest number of deals
    if (
        "most deals" in question
        or "maximum deals" in question
        or "highest number of deals" in question
        or "most number of deals" in question
    ):

        result = pipeline_by_sector(deals)

        if len(result) == 0:
            return "No sector data is available."

        top = result.sort_values(
            "deal_count",
            ascending=False
        ).iloc[0]

        return (
            f"{top['sector']} has the most deals, "
            f"with {int(top['deal_count'])} deals."
        )

    # Highest deal value by sector
    if (
        "highest deal value" in question
        or "highest value sector" in question
        or "sector with the highest value" in question
        or "industry with the highest value" in question
    ):

        result = pipeline_by_sector(deals)

        if len(result) == 0:
            return "No sector data is available."

        top = result.sort_values(
            "pipeline_value",
            ascending=False
        ).iloc[0]

        return (
            f"The sector with the highest recorded deal value is "
            f"{top['sector']}, with approximately "
            f"₹{top['pipeline_value']:,.2f} across "
            f"{int(top['deal_count'])} deals."
        )

    # General sector question
    if "sector" in question or "industry" in question:

        result = pipeline_by_sector(deals)

        if len(result) == 0:
            return "No sector data is available."

        top = result.sort_values(
            "pipeline_value",
            ascending=False
        ).iloc[0]

        return (
            f"The sector with the highest recorded deal value is "
            f"{top['sector']}, with approximately "
            f"₹{top['pipeline_value']:,.2f} across "
            f"{int(top['deal_count'])} deals."
        )

    # -------------------------------------------------
    # STAGE ANALYSIS
    # -------------------------------------------------

    if "stage" in question:

        result = pipeline_by_stage(deals)

        if len(result) == 0:
            return "No stage data is available."

        # Exclude lost deals from active stage analysis
        result = result[
            result["stage"].str.lower().str.strip()
            != "l. project lost"
        ]

        if len(result) == 0:
            return "No active stage data is available."

        top = result.sort_values(
            "pipeline_value",
            ascending=False
        ).iloc[0]

        return (
            f"The deal stage with the highest value is "
            f"{top['stage']}, with approximately "
            f"₹{top['pipeline_value']:,.2f} "
            f"across {int(top['deal_count'])} deals."
        )

    # -------------------------------------------------
    # PIPELINE SUMMARY
    # -------------------------------------------------

    if "pipeline" in question or "deal value" in question:

        summary = pipeline_summary(deals)

        active_stages = [
            "A. Lead Generated",
            "B. Sales Qualified Leads",
            "C. Demo Done",
            "D. Feasibility",
            "E. Proposal/Commercials Sent",
            "F. Negotiations",
            "G. Project Won",
            "H. Work Order Received",
            "I. POC",
            "J. Invoice sent",
            "K. Amount Accrued",
        ]

        active = deals[
            deals["stage"].isin(active_stages)
        ]

        active_pipeline = active["deal_value"].sum()

        return (
            f"Total deal records: {summary['total_deals']}. "
            f"Total recorded deal value is "
            f"₹{summary['total_pipeline']:,.2f}. "
            f"Active pipeline, excluding lost, on-hold and "
            f"irrelevant stages, is approximately "
            f"₹{active_pipeline:,.2f}."
        )

    # -------------------------------------------------
    # WORK ORDER COMPLETION
    # -------------------------------------------------

    if (
        "work order" in question
        or "work orders" in question
        or "completed" in question
        or "execution" in question
    ):

        summary = work_order_summary(orders)

        return (
            f"There are {summary['total_work_orders']} work orders. "
            f"{summary['completed_work_orders']} are "
            f"completed/executed, giving a completion rate of "
            f"{summary['completion_rate']}%."
        )

    # -------------------------------------------------
    # BILLING
    # -------------------------------------------------

    if (
        "billed" in question
        or "billing" in question
    ):

        summary = work_order_summary(orders)

        return (
            f"Total billed value is approximately "
            f"₹{summary['total_billed']:,.2f}."
        )

    # -------------------------------------------------
    # COLLECTIONS
    # -------------------------------------------------

    if (
        "collected" in question
        or "collection" in question
    ):

        summary = work_order_summary(orders)

        return (
            f"Total collected amount is approximately "
            f"₹{summary['total_collected']:,.2f}."
        )

    # -------------------------------------------------
    # RECEIVABLES
    # -------------------------------------------------

    if (
        "receivable" in question
        or "receivables" in question
        or "outstanding" in question
    ):

        summary = work_order_summary(orders)

        return (
            f"Total amount receivable is approximately "
            f"₹{summary['total_receivable']:,.2f}."
        )

    # -------------------------------------------------
    # UNKNOWN QUESTION
    # -------------------------------------------------

    return (
        "I can currently answer questions about pipeline, "
        "deal sectors, deal stages, work-order completion, "
        "billing, collections, and receivables."
    )


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    print("Skylark BI Query Engine")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":
            break

        try:

            answer = answer_query(question)

            print("\nAgent:", answer)
            print()

        except Exception as e:

            print("\nError:", e)
            print()