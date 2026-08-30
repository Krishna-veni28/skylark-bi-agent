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

    if "sector" in question or "industry" in question:

        result = pipeline_by_sector(deals)

        if len(result) == 0:
            return "No sector data is available."

        # Most deals / highest number of deals
        if (
            "most deals" in question
            or "maximum deals" in question
            or "highest number of deals" in question
            or "most number of deals" in question
            or "more deals" in question
            or "largest number of deals" in question
        ):
            top = result.sort_values(
                "deal_count",
                ascending=False
            ).iloc[0]

            return (
                f"{top['sector']} has the most deals, "
                f"with {int(top['deal_count'])} deals."
            )

        # Fewest deals / lowest number of deals
        if (
            "fewest deals" in question
            or "least deals" in question
            or "minimum deals" in question
            or "lowest number of deals" in question
            or "least number of deals" in question
        ):
            bottom = result.sort_values(
                "deal_count",
                ascending=True
            ).iloc[0]

            return (
                f"{bottom['sector']} has the fewest deals, "
                f"with {int(bottom['deal_count'])} deals."
            )

        # Lowest deal value
        if (
            "lowest deal value" in question
            or "least deal value" in question
            or "minimum deal value" in question
            or "smallest deal value" in question
        ):
            bottom = result.sort_values(
                "pipeline_value",
                ascending=True
            ).iloc[0]

            return (
                f"{bottom['sector']} has the lowest recorded "
                f"deal value at ₹{bottom['pipeline_value']:,.2f}, "
                f"across {int(bottom['deal_count'])} deals."
            )

        # Highest deal value
        if (
            "highest deal value" in question
            or "largest deal value" in question
            or "maximum deal value" in question
            or "highest value" in question
            or "largest value" in question
        ):
            top = result.sort_values(
                "pipeline_value",
                ascending=False
            ).iloc[0]

            return (
                f"{top['sector']} currently has the highest "
                f"recorded deal value at "
                f"₹{top['pipeline_value']:,.2f}, "
                f"across {int(top['deal_count'])} deals."
            )

        # Default sector question
        top = result.sort_values(
            "pipeline_value",
            ascending=False
        ).iloc[0]

        return (
            f"{top['sector']} currently has the highest "
            f"recorded deal value at "
            f"₹{top['pipeline_value']:,.2f}, "
            f"across {int(top['deal_count'])} deals."
        )

    # -------------------------------------------------
    # STAGE ANALYSIS
    # -------------------------------------------------

    if "stage" in question:

        result = pipeline_by_stage(deals)

        if len(result) == 0:
            return "No stage data is available."

        # Highest stage value
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