import os
import requests
import json
from urllib.parse import quote

# `search_fusionbase`: A function to search for companies in Fusionbase
# Parameters:
# - company_name: The name of the company to search.
# - source_key: The default source key (German Handelsregister by default).
# - filter_source_keys: List of source keys to exclude from the search results (UK Business registry by default).
def search_fusionbase(company_name, source_key="1051122944", filter_source_keys=["1784627846"]):
    """
    Searches for a company in Fusionbase, optionally filtering out specific sources.
    
    :param company_name: str - The name of the company to search for.
    :param source_key: str - The source key for filtering the search results.
    :param filter_source_keys: list - Source keys to exclude from the search results.
    :return: dict - A filtered list of search results from the Fusionbase API.
    """
    # Step 1: URL-encode the company name for safe API requests
    encoded_company_name = quote(company_name)

    # Step 2: Construct the search URL based on whether a source key is provided
    url = (f"https://api.fusionbase.com/api/v2/search/entities/organization?q={encoded_company_name}&source_key={source_key}"
           if source_key else f"https://api.fusionbase.com/api/v2/search/entities/organization?q={encoded_company_name}")

    # Step 3: Set up the request headers with the Fusionbase API key
    headers = {
        'X-API-KEY': os.getenv('FUSIONBASE_API_KEY'),
        'Content-Type': 'application/json; charset=utf-8',
    }

    # Step 4: Make the GET request to the Fusionbase API
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if the response is successful
    response_json = response.json()  # Parse the response JSON

    # Step 5: Filter out results with unwanted source keys
    filtered_results = {
        "results": [
            result for result in response_json.get("results", [])
            if result["entity"]["source_key"] not in filter_source_keys
        ]
    }

    # Step 6: Return the filtered results
    return filtered_results


# `get_entity`: A function to fetch detailed information about a specific entity in Fusionbase
# Parameters:
# - entity_id: The ID of the entity to retrieve.
# - entity_type: The type of entity (organization by default).
def get_entity(entity_id, entity_type="organization"):
    """
    Retrieves detailed information about an entity from Fusionbase.

    :param entity_id: str - The entity ID to fetch.
    :param entity_type: str - The type of the entity (e.g., organization).
    :return: dict - The entity details from the Fusionbase API.
    """
    if entity_id is None:
        return None  # Early return if no entity ID is provided

    # Step 1: Construct the URL for fetching the entity details
    url = f"https://api.fusionbase.com/api/v2/entities/{entity_type}/get/{entity_id}"

    # Step 2: Set up the request headers with the Fusionbase API key
    headers = {
        'X-API-KEY': os.getenv('FUSIONBASE_API_KEY'),
        'Content-Type': 'application/json; charset=utf-8',
    }

    # Step 3: Make the GET request to retrieve the entity details
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Step 4: If successful, return the entity details as JSON
        return response.json()
    else:
        # Step 5: If the request fails, log an error message
        print(f"Error: {response.status_code} - Unable to fetch entity {entity_id}")
        return None  # Return None on error


# `get_relation_data`: A function to retrieve relationship data for an entity
# Parameters:
# - entity_id: The ID of the entity whose relations we want to fetch.
# - relation_id: The ID of the specific relation to resolve.
def get_relation_data(entity_id, relation_id):
    """
    Resolves and retrieves specific relation data for an entity from Fusionbase.

    :param entity_id: str - The entity ID to fetch the relations for.
    :param relation_id: str - The relation ID to resolve.
    :return: dict or None - The resolved relation data, or None if an error occurs.
    """
    if not entity_id or not relation_id:
        return None  # Early return if no entity_id or relation_id is provided

    # Step 1: Construct the URL for fetching the relation data
    url = f"https://api.fusionbase.com/api/v2/relation/resolve/{relation_id}/{entity_id}"

    # Step 2: Set up the request headers with the Fusionbase API key
    headers = {
        'X-API-KEY': os.getenv('FUSIONBASE_API_KEY'),
        'Content-Type': 'application/json; charset=utf-8'
    }

    # Step 3: Make the POST request to retrieve the relation data
    try:
        response = requests.post(url, headers=headers, timeout=120)  # 120-second timeout for large requests
        response.raise_for_status()  # Check if the response is successful
        data = response.json()  # Parse the response JSON

        # Step 4: Return the first result's entity value if available
        return data[0].get("entity", {}).get("value", {})
    except (requests.exceptions.RequestException, IndexError, KeyError) as e:
        # Step 5: Handle any exceptions, including request timeouts or missing data
        print(f"Error fetching relation data for entity {entity_id} and relation {relation_id}: {e}")
        return None  # Return None on error


# `invoke_service`: A function to invoke a service from Fusionbase API with entity details.
# Parameters:
# - entity_name: The name of the entity (e.g., company name) to provide as input to the service.
# - postal_code: The postal code of the entity's address.
# - street: The street address of the entity.
# - city: The city where the entity is located.
# - service_key: The service key for the specific service to invoke (defaults to 4658603456 which is the Web context).
# Returns:
# - A dictionary containing the API response from the Fusionbase service. If the request fails, it returns None.

def invoke_service(entity_name, postal_code, street, city, service_key="4658603456"):
    """
    Invokes a service using the Fusionbase API with entity details.

    :param entity_name: str - The name of the entity (e.g., company name).
    :param postal_code: str - The postal code of the entity's address.
    :param street: str - The street address of the entity.
    :param city: str - The city of the entity.
    :param service_key: str - The service key to use for invocation (default is 4658603456).
    :return: dict - The response from the Fusionbase API service.
    """
    # Step 1: Prepare the API URL
    url = "https://api.fusionbase.com/api/v2/service/invoke"

    # Step 2: Set up the request headers with the Fusionbase API key
    headers = {
        "X-API-KEY": os.getenv("FUSIONBASE_API_KEY"),  # Fetch the API key from environment variables
        "Content-Type": "application/json; charset=utf-8"
    }

    # Step 3: Define the payload with the input data and the service key
    payload = {
        "inputs": {
            "entity_name": entity_name,
            "postal_code": postal_code,
            "street": street,
            "city": city
        },
        "service_key": service_key
    }

    # Step 4: Make the POST request to the Fusionbase API
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception if the request was not successful
        
        # Step 5: Parse the response JSON and return it
        return response.json()

    except requests.exceptions.RequestException as e:
        # Handle any exceptions such as timeouts or connection errors
        print(f"Error invoking service: {e}")
        return None