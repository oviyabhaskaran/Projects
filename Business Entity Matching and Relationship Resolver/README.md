Overview

This project is a Python-based application designed to match and validate Company Names, particularly when multiple names may refer to the same entity (e.g., due to mergers or acquisitions). By using Bing Custom Search API, the program identifies and retrieves relevant reference URLs for paired company names, providing insights into whether two names represent the same company or different entities. The application also generates a well-formatted Excel report containing the input company names and the corresponding reference URLs, applying advanced formatting for readability.

Key Features

Cleans and normalizes company names by removing special characters and non-English text.
Searches the web using Bing Custom Search API to find relevant references for paired company names.
Outputs an Excel file (output.xlsx) with up to 5 top referral URLs for each pair.
Enhances readability with advanced Excel formatting (colored headers, aligned text, and URL highlights).

Setup Prerequisites:

Python 3.8 or higher
Install required libraries
Prepare input.xlsx with two columns:
  Old Name: Previous company name.
  New Name: Current or alternate name.
Bing API Configuration: Get an API key and Custom Search Engine ID from the Bing Custom Search API portal.
output.xlsx: contains the cleaned company names and referral URLs.
