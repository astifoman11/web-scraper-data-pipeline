import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# Load clinics with websites
df = pd.read_excel("Paediatrician_Clinics_Melbourne.xlsx")

# Basic email detection
email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# Prepare output columns
df["Primary Email"] = ""
df["All Emails"] = ""

# Common paths where emails are usually listed
paths_to_try = ["", "/contact", "/contact-us", "/about", "/about-us"]
headers = {"User-Agent": "Mozilla/5.0"}

for i, row in df.iterrows():
    base_url = str(row.get("Website", "")).strip().rstrip("/")

    if not base_url.startswith("http"):
        df.at[i, "Primary Email"] = "No website"
        continue

    emails_found = set()

    for path in paths_to_try:
        url = base_url + path
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            # Extract from mailto links
            mailto = [a["href"].replace("mailto:", "") for a in soup.select('a[href^=mailto]')]
            emails_found.update(mailto)

            # Extract from raw HTML via regex
            matches = email_pattern.findall(res.text)
            emails_found.update(matches)

        except Exception:
            continue

    emails = list(emails_found)
    df.at[i, "Primary Email"] = emails[0] if emails else "Not found"
    df.at[i, "All Emails"] = ", ".join(emails)

    print(f"[{i+1}/{len(df)}] {row['Clinic Name']} → {df.at[i, 'Primary Email']}")
    time.sleep(2)  # avoid triggering rate-limiting or firewalls

# Save result
df.to_excel("GP_Clinics_With_Emails_Expanded.xlsx", index=False)
print("Done! Saved to GP_Clinics_With_Emails_Expanded.xlsx")
