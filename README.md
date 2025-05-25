# Allied Health & Clinic Data Pipeline

This project automates the discovery, enrichment, and loading of health clinic data (GPs, paediatricians, allied health, NDIS providers) across Melbourne using the Google Places API and web scraping with beautifulsoup4.

---

## Features

- Search clinics by suburb and type (e.g., GP, Allied Health, NDIS Therapy, Paediatricians)
- Enrich clinics with phone numbers and websites using the Google Place Details API
- Scrape clinic websites for email addresses
- Upload results to an Excel sheet

---

## Project Structure

| File | Description |
|------|-------------|
| `U&I Places API.py` | Searches GP and paediatrician clinics, enriches with phone + website |
| `email_search_GPs.py` | Scrapes websites from Excel file to extract emails |
| `SQL_excel.py` | Uploads Excel file into a PostgreSQL table |
| `PlacesAPI_AlliedHealth.py` | Scrapes Allied Health and NDIS providers across suburbs |
| `GP_Clinics_Final.xlsx` | Sample output with clinic data |
| `README.md` | Project documentation |

---

## Requirements

Install dependencies:

```bash
pip install requests pandas openpyxl psycopg2 sqlalchemy beautifulsoup4 tqdm
