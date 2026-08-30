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


print("Loading Deals...")
deals_raw = get_deals()
deals_df = clean_board(deals_raw)
deals = prepare_deals(deals_df)

print("\n========== PIPELINE SUMMARY ==========")
print(pipeline_summary(deals))

print("\n========== PIPELINE BY SECTOR ==========")
print(pipeline_by_sector(deals).to_string(index=False))

print("\n========== PIPELINE BY STAGE ==========")
print(pipeline_by_stage(deals).to_string(index=False))


print("\n\nLoading Work Orders...")
orders_raw = get_work_orders()
orders_df = clean_board(orders_raw)
orders = prepare_work_orders(orders_df)

print("\n========== WORK ORDER SUMMARY ==========")
print(work_order_summary(orders))