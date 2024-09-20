# Fusionbase Examples

This repository contains example use cases that demonstrate how to use the Fusionbase API to enrich business data. Fusionbase aggregates data from various public and proprietary sources, enabling users to enhance their datasets with valuable insights such as financial data, web context, network information, and news articles.

## Enrichments

The examples in this repository show how to enrich company data by retrieving relevant external information from Fusionbase. These examples highlight how to use the API to:

- **Web Context Data**: Retrieve live web-related data about companies, including their online presence and activities.
- **Financial KPIs and Statements**: Enrich your dataset with financial key performance indicators, balance sheets, and income statements.
- **Network and Management Relations**: Fetch relationships and network data, such as partnerships and active management teams, to get a deeper view of a company’s connections.
- **News and Events**: Pull the latest news articles or mentions related to companies, providing timely insights about their public reputation and significant events.

### Key Use Cases

1. **Enriching Arbitrary Companies**: You can use the Fusionbase API to gather a variety of data points for companies, even if they are not available as entities within Fusionbase. This is especially useful for small or unregistered companies. By providing basic information such as company name and address, you can retrieve live web data.  

3. **Cross-Referencing with External Data**: The examples show how you can cross-reference existing datasets with Fusionbase to enhance business profiles, provide context for decision-making, or build comprehensive reports on companies. This includes retrieving their financial health, key personnel, and even their digital footprint.

### Example Workflow

1. **Company Identification**: Each example begins by identifying companies based on basic attributes like name and address. This information is used to search for and retrieve data from Fusionbase.
   
2. **Data Retrieval**: The API is used to request various types of data—web, financial, network, and news. Depending on the available information for each company, different types of data can be retrieved.
   
3. **Data Enrichment**: Once retrieved, the external data is added to the original dataset, enriching each company profile with new insights.

4. **Exporting Results**: The enriched datasets are saved into structured formats (e.g., CSV files), allowing for further analysis, reporting, or integration into other workflows.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Fusionbase API Key (set as an environment variable `FUSIONBASE_API_KEY`)
- Required Python packages (pandas, requests)