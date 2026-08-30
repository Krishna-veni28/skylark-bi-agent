import os
from query_engine import load_data
from bi_engine import (
    pipeline_summary,
    pipeline_by_sector,
    pipeline_by_stage,
    work_order_summary,
)


def get_business_context():
    """
    Load the latest data from Monday.com and prepare
    a compact business context for the agent.
    """

    deals, orders = load_data()

    context = {}

    # Pipeline
    pipeline = pipeline_summary(deals)
    context["pipeline"] = pipeline

    # Sector
    sector_data = pipeline_by_sector(deals)
    context["sector_data"] = sector_data.to_dict("records")

    # Stage
    stage_data = pipeline_by_stage(deals)
    context["stage_data"] = stage_data.to_dict("records")

    # Work orders
    work_orders = work_order_summary(orders)
    context["work_orders"] = work_orders

    return context


def answer_business_question(question):
    """
    Basic founder-level business question router.

    The data is fetched dynamically from Monday.com.
    """

    question = question.lower().strip()

    try:
        context = get_business_context()

    except Exception as e:
        return (
            "I couldn't retrieve the latest data from Monday.com. "
            "Please check the connection and try again."
        )

    pipeline = context["pipeline"]
    sectors = context["sector_data"]
    stages = context["stage_data"]
    work_orders = context["work_orders"]

    # -------------------------------------------------
    # PIPELINE
    # -------------------------------------------------

    if "pipeline" in question:

        total = pipeline.get("total_pipeline", 0)

        return (
            f"Our total recorded deal value is "
            f"₹{total:,.2f}. "
            f"There are {pipeline.get('total_deals', 0)} "
            f"deal records in the system."
        )

    # -------------------------------------------------
    # SECTOR
    # -------------------------------------------------

    if "sector" in question or "industry" in question:

        if not sectors:
            return "Sector information is currently unavailable."

        top_sector = max(
            sectors,
            key=lambda x: x.get("pipeline_value", 0)
        )

        return (
            f"{top_sector.get('sector', 'Unknown')} currently has "
            f"the highest recorded deal value at "
            f"₹{top_sector.get('pipeline_value', 0):,.2f}, "
            f"across {int(top_sector.get('deal_count', 0))} deals."
        )

    # -------------------------------------------------
    # DEAL STAGE
    # -------------------------------------------------

    if "stage" in question:

        if not stages:
            return "Deal-stage information is currently unavailable."

        top_stage = max(
            stages,
            key=lambda x: x.get("pipeline_value", 0)
        )

        return (
            f"The highest-value deal stage is "
            f"{top_stage.get('stage', 'Unknown')}, "
            f"with approximately "
            f"₹{top_stage.get('pipeline_value', 0):,.2f} "
            f"across {int(top_stage.get('deal_count', 0))} deals."
        )

    # -------------------------------------------------
    # WORK ORDERS
    # -------------------------------------------------

    if (
        "work order" in question
        or "work orders" in question
        or "operations" in question
        or "execution" in question
    ):

        return (
            f"There are {work_orders.get('total_work_orders', 0)} "
            f"work orders. "
            f"{work_orders.get('completed_work_orders', 0)} are "
            f"completed, giving a completion rate of "
            f"{work_orders.get('completion_rate', 0)}%."
        )

    # -------------------------------------------------
    # COLLECTIONS
    # -------------------------------------------------

    if (
        "collection" in question
        or "collected" in question
    ):

        return (
            f"The total amount collected is approximately "
            f"₹{work_orders.get('total_collected', 0):,.2f}."
        )

    # -------------------------------------------------
    # RECEIVABLES
    # -------------------------------------------------

    if (
        "receivable" in question
        or "receivables" in question
        or "outstanding" in question
    ):

        return (
            f"The current receivable amount is approximately "
            f"₹{work_orders.get('total_receivable', 0):,.2f}."
        )

    # -------------------------------------------------
    # BILLING
    # -------------------------------------------------

    if (
        "billing" in question
        or "billed" in question
    ):

        return (
            f"The total billed value is approximately "
            f"₹{work_orders.get('total_billed', 0):,.2f}."
        )

    # -------------------------------------------------
    # LEADERSHIP SUMMARY
    # -------------------------------------------------

    if (
        "leadership" in question
        or "founder" in question
        or "executive" in question
        or "summary" in question
    ):

        return (
            "Leadership snapshot:\n"
            f"- Deals: {pipeline.get('total_deals', 0)}\n"
            f"- Recorded deal value: "
            f"₹{pipeline.get('total_pipeline', 0):,.2f}\n"
            f"- Work orders: "
            f"{work_orders.get('total_work_orders', 0)}\n"
            f"- Work-order completion: "
            f"{work_orders.get('completion_rate', 0)}%\n"
            f"- Total billed: "
            f"₹{work_orders.get('total_billed', 0):,.2f}\n"
            f"- Total collected: "
            f"₹{work_orders.get('total_collected', 0):,.2f}\n"
            f"- Total receivable: "
            f"₹{work_orders.get('total_receivable', 0):,.2f}"
        )

    # -------------------------------------------------
    # UNKNOWN QUESTION
    # -------------------------------------------------

    return (
        "I can help with business questions about "
        "pipeline, sectors, deal stages, work orders, "
        "billing, collections, receivables, and "
        "leadership summaries."
    )


# =====================================================
# TEST AGENT
# =====================================================

if __name__ == "__main__":

    print("Skylark Business Intelligence Agent")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower().strip() == "exit":
            break

        answer = answer_business_question(question)

        print("\nAgent:")
        print(answer)
        print()