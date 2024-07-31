# import requests

# # OpenFDA API endpoint for drug names
# url = "https://api.fda.gov/drug/"

# # Parameters to fetch a list of drug names
# params = {
#     "count": "openfda.brand_name.exact",
#     "limit": 100000  # Limit the results to 100 for simplicity
# }

# # Sending the GET request to the API
# response = requests.get(url, params=params)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     drug_names = [item['term'] for item in data['results']]
#     print(len(drug_names))
#     #print(drug_names)
# else:
#     print(f"Error: {response.status_code}")
# import requests

# # RxNorm API endpoint to get a list of drugs
# url = "https://rxnav.nlm.nih.gov/REST/allconcepts.json?tty=IN+MIN+BN+PIN"

# # Sending the GET request to the API
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     drug_names = [concept['name'] for concept in data['minConceptGroup']['minConcept']]
#     print(len(drug_names))  # Print the first 100 drug names for simplicity
# else:
#     print(f"Error: {response.status_code}")
# import requests

# # NHS API endpoint for medicines
# url = "https://api.nhs.uk/medicines/acamol"

# # Headers for the request including the API key
# headers = {
#     "subscription-key": "YOUR_API_KEY"  # Replace with your NHS API key
# }

# # Sending the GET request to the API
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print(f"Error: {response.status_code}")
# import requests
# from bs4 import BeautifulSoup

# # URL of the Israeli Drug Registry page
# url = "https://israeldrugs.health.gov.il/#!/byDrug"

# # Make a request to the webpage
# response = requests.get(url)

# # Parse the HTML content of the page
# soup = BeautifulSoup(response.content, 'html.parser')

# # Example: Extract drug names
# drug_names = []
# for drug in soup.find_all('div', class_='drug-name'):
#     drug_names.append(drug.text.strip())

# # Print the drug names
# for name in drug_names:
#     print(name)


import requests

def get_drug_info(drug_name):
    api_key = "your_api_key_here"  # Replace with your OpenFDA API key
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results'][0]
        else:
            return "No results found."
    else:
        return f"Error: {response.status_code}"

def extract_important_info(drug_data):
    important_info = {
        "Brand Name": drug_data.get("openfda", {}).get("brand_name", ["N/A"])[0],
        "Generic Name": drug_data.get("openfda", {}).get("generic_name", ["N/A"])[0],
        "Manufacturer": drug_data.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
        "Active Ingredients": drug_data.get("active_ingredient", ["N/A"]),
        "Purpose": drug_data.get("purpose", ["N/A"]),
        "Indications and Usage": drug_data.get("indications_and_usage", ["N/A"]),
        "Warnings": drug_data.get("warnings", ["N/A"]),
        "Dosage and Administration": drug_data.get("dosage_and_administration", ["N/A"]),
        "Inactive Ingredients": drug_data.get("inactive_ingredient", ["N/A"])
    }
    return important_info

def display_info(info):
    for key, value in info.items():
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                print(f"  - {item}")
        else:
            print(f"  - {value}")
        print()

drug_name = "Advil"
drug_data = get_drug_info(drug_name)
if isinstance(drug_data, dict):
    important_info = extract_important_info(drug_data)
    display_info(important_info)
else:
    print(drug_data)
