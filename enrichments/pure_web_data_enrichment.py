# `enrich_companies_with_web_context`: A script that enriches a list of companies with web context data from Fusionbase.
# This script allows arbitrary companies to be enriched with web context data, even if they do not exist as a Fusionbase entity.
# It is particularly useful for small companies not registered in public databases like the Handelsregister.
# The service invoked uses the web context service with the service key `4658603456`.
# The results are saved as a CSV file for further analysis.

import pandas as pd
from utils import invoke_service

if __name__ == '__main__':
    try:
        # Attempt to import the `rich` library for pretty printing in the terminal.
        from rich import print
    except ImportError:
        # If the rich library is not installed, guide the user to install it.
        print("Please install the rich library using 'pip install rich' to see the formatted output.")
    
    # Step 1: Load the data from the `companies.csv` file.
    # The `postal_code` is read as a string to maintain leading zeros in some postal codes.
    companies = pd.read_csv('data/companies.csv', dtype={"postal_code": str}).to_dict(orient='records')

    # Step 2: Iterate over each company in the loaded dataset.
    for company in companies:
        # print(company)  # Print the company details for reference during processing.

        # Step 3: Invoke the web context service using the `invoke_service` function.
        # The service key `4658603456` is used for this particular service (Company Web Context).
        # No guarantee is given on the returned data points as the service gathers the data live.
        web_data = invoke_service(
            company['name'], 
            company['postal_code'], 
            company['street'], 
            company['city'], 
            service_key="4658603456"
        )

        # Step 4: If web data is returned, add it to the company's record.
        if web_data:
            company["web_data"] = web_data.get("data")

    # Step 5: Convert the list of enriched companies back to a DataFrame.
    result_df = pd.DataFrame(companies)

    # Step 6: Save the enriched data to a CSV file for later analysis.
    result_df.to_csv('data/enriched_companies_via_web_query.csv', index=False)
