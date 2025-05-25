import requests
import pandas as pd
import time
from tqdm import tqdm

# Replace with your actual Google Places API key
API_KEY = "YOUR_GOOGLE_API_KEY"

# Melbourne corridor suburbs
SUBURBS = [
    "Werribee", "Hoppers Crossing", "Point Cook", "Tarneit", "Truganina", "Laverton", "Altona", "Newport", "Williamstown",
    "Footscray", "Yarraville", "Seddon", "Maribyrnong", "Kensington", "Flemington", "North Melbourne", "Melbourne CBD",
    "Carlton", "Fitzroy", "Brunswick", "Northcote", "Preston", "Thornbury", "Reservoir", "South Yarra", "Toorak", "Prahran",
    "St Kilda", "Malvern", "Caulfield", "Glen Huntly", "Carnegie", "Murrumbeena", "Camberwell", "Box Hill", "Burwood",
    "Blackburn", "Glen Waverley", "Mount Waverley", "Chadstone", "Clayton", "Springvale", "Noble Park", "Dandenong",
    "Keysborough", "Endeavour Hills", "Berwick", "Officer", "Pakenham"
]

# Search terms to combine with suburbs
SEARCH_TERMS = ["Allied Health", "NDIS Therapy"]

# Google API endpoints
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

results = []

# Loop through suburbs and search terms
for suburb in tqdm(SUBURBS, desc="Processing suburbs"):
    for term in SEARCH_TERMS:
        query = f"{term} {suburb} VIC"
        params = {"query": query, "region": "au", "key": API_KEY}

        try:
            res = requests.get(BASE_URL, params=params)
            res.raise_for_status()
            places = res.json().get("results", [])

            for place in places:
                place_id = place.get("place_id")
                details_params = {
                    "place_id": place_id,
                    "fields": "formatted_phone_number,website",
                    "key": API_KEY
                }

                details_res = requests.get(DETAILS_URL, params=details_params)
                details = details_res.json().get("result", {}) if details_res.status_code == 200 else {}

                results.append({
                    "Suburb Searched": suburb,
                    "Search Term": term,
                    "Clinic Name": place.get("name"),
                    "Address": place.get("formatted_address"),
                    "Rating": place.get("rating", ""),
                    "Phone": details.get("formatted_phone_number", ""),
                    "Website": details.get("website", "")
                })

            time.sleep(2)  # Respect rate limits

        except Exception as e:
            print(f"Error on query '{query}': {e}")
            continue

# Save to Excel
df = pd.DataFrame(results)
df.drop_duplicates(subset=["Clinic Name", "Address"], inplace=True)
df.to_excel("Allied_Health_NDIS_Therapy_Melbourne.xlsx", index=False)
print("Saved: Allied_Health_NDIS_Therapy_Melbourne.xlsx")
