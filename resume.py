import requests
import os
from serpapi import GoogleSearch


# Function to search multiple resumes using SerpAPI
def search_resumes(name):
    api_key = "API_KEY"  # Replace with your actual SerpAPI key
    search_query = f"{name} resume filetype:pdf"

    params = {
        "q": search_query,
        "engine": "google",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract all PDF links
    pdf_links = [result["link"] for result in results.get("organic_results", []) if result["link"].endswith(".pdf")]

    return pdf_links


# Function to download multiple resumes into a folder
def download_resumes(name):
    pdf_urls = search_resumes(name)

    if not pdf_urls:
        print("No resumes found!")
        return

    # Create folder if not exists
    folder_name = f"resumes/{name.replace(' ', '_')}"
    os.makedirs(folder_name, exist_ok=True)

    # Download each resume
    for idx, pdf_url in enumerate(pdf_urls, start=1):
        try:
            print(f"Downloading: {pdf_url} ...")
            response = requests.get(pdf_url, timeout=10)  # Set timeout to avoid hanging
            if response.status_code == 200:
                filename = os.path.join(folder_name, f"{name.replace(' ', '_')}_resume_{idx}.pdf")
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"✅ Downloaded: {filename}")
            else:
                print(f"⚠️ Skipped (Invalid Response): {pdf_url}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Skipped (Error): {pdf_url} - {e}")


# User input for name
name = input("Enter the name to search resumes: ")
download_resumes(name)
