from monday_client import get_deals
from data_cleaner import clean_board

deals_raw = get_deals()
deals_df = clean_board(deals_raw)

print("\nDeal Value samples:")
print(deals_df["deal_value"].head(20).to_string())

print("\nForecast Value samples:")
print(deals_df["deal_forecast_value"].head(20).to_string())

print("\nClose Probability samples:")
print(deals_df["deal_close_probability"].head(20).to_string())