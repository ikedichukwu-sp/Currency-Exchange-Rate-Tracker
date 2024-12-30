import datetime
import requests
import os


# Fetch the API key from the environment variables
api_key = os.getenv("API_KEY")

# Check if the API key is present
if not api_key:
    print("API key not found in environment variables.")
    exit()

# API URL
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"



# Fetch API data
response = requests.get(url)
now = datetime.datetime.now()

if response.status_code == 200:
    data = response.json()

    print("\nWelcome to the Currency Exchange Rate Tracker")

    # Display base currency
    currency_base = data.get('base_code')
    print(f"Base Currency: {currency_base}\n")

    # Display available currencies dynamically
    available_currency = ", ".join(data.get('conversion_rates', {}).keys())
    print(f"Available currencies: {available_currency}\n")

    # Include the loop for iterating over conversion rates
    print("Currency Conversion Rates:")
    for currency, rate in data.get('conversion_rates', {}).items():
        cu_rate = (f"  {currency}: {rate}")
        # print(f"{cu_rate}")

    print()  # Add a line break for better readability

    # Get target currency from user
    while True:
        target_currency = input("Enter target currency (e.g., EUR): ").upper().strip()

        # Validate the target currency
        if target_currency not in data.get('conversion_rates', {}):
            print("Invalid target currency. Please try again.")
        else:
            break  # Exit the loop if the currency is valid

    # Get amount to convert
    try:
        amount = float(input(f"Enter the amount in {currency_base}: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        exit()

    # Perform conversion
    rate = data['conversion_rates'][target_currency]
    print(f"1 {currency_base} = {rate} {target_currency}")
    total_rate = amount * rate
    convert_result = f"{amount} {currency_base} = {total_rate:.2f} {target_currency}"
    print("\nConversion Results:")
    print(convert_result)


    # Save results to a file
    data_to_save = f"""
Base currency: {currency_base}
Amount: {amount}
{convert_result}
Timestamp: {now.strftime("%Y-%m-%d %H:%M:%S")}
"""
    with open("currency_conversion_results.txt", "w") as file:
        file.write(data_to_save)

    print("\nConversion results saved to 'currency_conversion_results.txt'")
else:
    print("Failed to fetch exchange rate data. Please try again later.")
