import requests
import pandas as pd
import time
from pathlib import Path

# Set your Google Places API key
API_KEY = "YOUR_GOOGLE_API_KEY"

# Suburbs across Melbourne's growth corridor
SUBURBS = [
    "Werribee", "Hoppers Crossing", "Point Cook", "Tarneit", "Truganina", "Laverton", "Altona", "Newport", "Williamstown",
    "Footscray", "Yarraville", "Seddon", "Maribyrnong", "Kensington", "Flemington", "North Melbourne", "Melbourne CBD",
    "Carlton", "Fitzroy", "Brunswick", "Northcote", "Preston", "Thornbury", "Reservoir", "South Yarra", "Toorak", "Prahran",
    "St Kilda", "Malvern", "Caulfield", "Glen Huntly", "Carnegie", "Murrumbeena", "Camberwell", "Box Hill", "Burwood",
    "Blackburn", "Glen Waverley", "Mount Waverley", "Chadstone", "Clayton", "Springvale", "Noble Park", "Dandenong",
    "Keysborough", "Endeavour Hills", "Berwick", "Officer", "Pakenham"
]


def search_clinics(term: str, existing_file: str = None, delay: float = 2.0):
    """
    Uses Google Places Text Search to find clinics based on a search term and suburb.
    Optionally filters out existing clinics loaded from a previous Excel file.
    """
    new_records = []
    existing = set()

    # Load existing clinics to avoid duplicates
    if existing_file and Path(existing_file).exists():
        df_existing = pd.read_excel(existing_file)
        existing = set(df_existing["Clinic Name"].str.lower())

    for suburb in SUBURBS:
        query = f"{term} clinic in {suburb}, VIC Australia"
        res = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json", params={
            "query": query,
            "key": API_KEY
        })

        data = res.json().get("results", [])

        for place in data:
            name = place.get("name", "").strip()
            if name.lower() in existing:
                continue  # Skip if clinic already exists

            new_records.append({
                "Suburb": suburb,
                "Clinic Name": name,
                "Address": place.get("formatted_address", ""),
                "Rating": place.get("rating", ""),
                "Place ID": place.get("place_id", "")
            })

        time.sleep(delay)  # Respect API rate limits

    return pd.DataFrame(new_records)


def enrich_clinic_details(df: pd.DataFrame, delay: float = 1.5):
    """
    Takes a DataFrame of clinics with Place IDs and fetches phone and website
    details using Google Place Details API.
    """
    df["Phone"] = ""
    df["Website"] = ""

    for i, row in df.iterrows():
        place_id = row["Place ID"]
        res = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params={
            "place_id": place_id,
            "fields": "formatted_phone_number,website",
            "key": API_KEY
        })

        result = res.json().get("result", {})
        df.at[i, "Phone"] = result.get("formatted_phone_number", "")
        df.at[i, "Website"] = result.get("website", "")

        time.sleep(delay)

    return df


def run_pipeline():
    """
    Coordinates the scraping and enrichment process for both GP and paediatrician clinics.
    Outputs final results into Excel files.
    """
    gp_existing_file = "GP_Clinics_Melbourne_Corridor.xlsx"
    output_gp_new = "New_GP_Clinics_From_Google_Places.xlsx"
    output_gp_enriched = "GP_Clinics_With_Website_And_Phone.xlsx"
    output_paeds = "Paediatrician_Clinics_Melbourne.xlsx"

    print("Fetching new GP clinics...")
    gp_df = search_clinics(term="GP", existing_file=gp_existing_file)
    if not gp_df.empty:
        gp_df.to_excel(output_gp_new, index=False)
        print(f"Saved {len(gp_df)} new GP clinics.")

        print("Enriching GP clinic details...")
        enriched_gp = enrich_clinic_details(gp_df)
        enriched_gp.to_excel(output_gp_enriched, index=False)
        print(f"Saved to {output_gp_enriched}")
    else:
        print("No new GP clinics found.")

    print("Fetching paediatrician clinics...")
    paed_df = search_clinics(term="paediatrician")
    if not paed_df.empty:
        enriched_paed = enrich_clinic_details(paed_df)
        enriched_paed.sort_values("Suburb").to_excel(output_paeds, index=False)
        print(f"Saved to {output_paeds}")
    else:
        print("No paediatrician clinics found.")


if __name__ == "__main__":
    run_pipeline()
