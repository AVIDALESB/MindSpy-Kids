import requests

class CountryAPI:
    def __init__(self):
        self.base_url = "https://restcountries.com/v3.1"
    
    def get_all_countries(self):
        try:
            response = requests.get(f"{self.base_url}/all", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching countries: {e}")
            return []
