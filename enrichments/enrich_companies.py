import pandas as pd
from utils import search_fusionbase, get_entity, get_relation_data
from sample_utils import extract_active_relations
from relations_map import (NETWORK_RELATION, FINANCIAL_KPIS_RELATION, 
                           FINANCIAL_BALANCE_SHEET_RELATION, 
                           FINANCIAL_PROFIT_AND_LOSS_RELATION, 
                           WEB_CONTEXT_RELATION, NEWS_RELATION)

# Importing necessary libraries and functions.
# `pandas` is used for data manipulation, while `utils` and `sample_utils` contain the custom functions for interacting with the Fusionbase API.
# `relations_map` defines the specific relationship types we are interested in querying.

if __name__ == '__main__':
    try:
        # Attempt to import the `rich` library for pretty printing in the terminal. 
        from rich import print
    except ImportError:
        print("Please install the rich library using 'pip install rich' to see the formatted output.")
    
    # Load the data from a CSV file that contains a list of companies.
    # Each company record will be processed individually to enrich its data.
    companies = pd.read_csv('data/companies.csv', dtype={"postal_code": str}).to_dict(orient='records')
    
    # Iterating through each company in the dataset
    for company in companies:
        # Step 1: Search for the company in Fusionbase using its name.
        search_results = search_fusionbase(company['name'], postal_code=company['postal_code'])

        # Step 2: Extract the Fusionbase entity ID if any results are found.
        fb_entity_id = search_results['results'][0]['entity']['fb_entity_id'] if search_results['results'] else None

        if not fb_entity_id:
            # If no entity ID was found, print a message and move to the next company.
            print(f"Company {company['name']} not found in Fusionbase.")
            continue

        # Step 3: Fetch the company's details (entity information) from Fusionbase using the entity ID.
        entity = get_entity(fb_entity_id)
        
        # Step 4: Fetch data related to the company's network, including management and partners.
        network_relation_data = get_relation_data(fb_entity_id, NETWORK_RELATION)

        # Step 5: Extract active management and partners from the network data.
        activate_mangement_and_partners = extract_active_relations(network_relation_data.get("links", []))

        # Step 6: Fetch financial KPIs related to the company.
        financial_kpi_relation_data = get_relation_data(fb_entity_id, FINANCIAL_KPIS_RELATION)
        print(financial_kpi_relation_data)

        # Step 7: Fetch the company's balance sheet data.
        balance_sheet_relation_data = get_relation_data(fb_entity_id, FINANCIAL_BALANCE_SHEET_RELATION)
        print(balance_sheet_relation_data)

        # Step 8: Fetch the company's income statement data.
        income_statement_relation_data = get_relation_data(fb_entity_id, FINANCIAL_PROFIT_AND_LOSS_RELATION)
        print(income_statement_relation_data)

        # Step 9: Fetch web context data related to the company (can take time).
        web_data_relation_data = get_relation_data(fb_entity_id, WEB_CONTEXT_RELATION)
        print(web_data_relation_data)

        # Step 10: Fetch recent news articles or mentions related to the company (can take time).
        news_relation_data = get_relation_data(fb_entity_id, NEWS_RELATION)
        print(news_relation_data)

        # Step 11: Enrich the original company dictionary with the fetched data.
        company["active_management"] = activate_mangement_and_partners
        company["financial_kpis"] = financial_kpi_relation_data
        company["balance_sheet"] = balance_sheet_relation_data
        company["income_statement"] = income_statement_relation_data
        company["web_data"] = web_data_relation_data
        company["news"] = news_relation_data

    # Step 12: Convert the list of enriched companies back to a DataFrame.
    result_df = pd.DataFrame(companies)

    # Step 13: Save the enriched data back into a CSV file for later analysis.
    result_df.to_csv('data/enriched_companies.csv', index=False)