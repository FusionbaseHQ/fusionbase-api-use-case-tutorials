def extract_active_relations(data):
    """
    Extracts active management and partnership relations from the provided data.
    
    Filters relationships based on specific criteria and returns relevant information
    in a structured format.
    
    :param data: list - A list of relationship dictionaries.
    :return: list - A list of extracted relationships with relevant details.
    """
    results = []  # Initialize an empty list to store the results
    geschaeftsfuehrer_found = False  # Boolean flag to track if 'Geschäftsführung' has been found

    # Step 1: Iterate over each relationship item in the input data
    for item in data:
        # Step 2: Only consider relationships with depth = 1 and no 'end_date' (i.e., active relationships)
        if item.get('depth') == 1 and item['meta'].get('end_date') is None:
            # Step 3: Identify the appropriate German label based on the relationship's label
            label = item.get('label', '')

            if any(keyword in label for keyword in ['MANAGING', 'BOARD', 'FULLY_LIABLE_PARTNER', 'OWNER']):
                # If the label matches any of these keywords, assign 'Geschäftsführung'
                german_label = 'Geschäftsführung'
                geschaeftsfuehrer_found = True  # Mark that a Geschäftsführer has been found
            elif 'PROCURA' in label:
                # If the label is 'PROCURA', only proceed if no Geschäftsführer was found
                if geschaeftsfuehrer_found:
                    continue  # Skip this relation if a Geschäftsführer was already found
                german_label = 'Prokura'
            else:
                # If the label doesn't match any relevant keyword, skip this item
                continue

            # Step 4: Construct a dictionary with the necessary details from the current relationship
            result = {
                "name": item['entity_from']['attributes']['display_name'].get('en', 'Unknown'),  # Fallback to 'Unknown' if name not found
                "fb_entity_id": item['entity_from'].get('fb_entity_id', 'Unknown'),  # Fallback to 'Unknown' if ID not found
                "label": label,
                "german_label": german_label
            }

            # Step 5: Append the constructed result to the results list
            results.append(result)

    # Step 6: Return the list of extracted relationships
    return results