import requests


class API_call():

    def get_euribordata():
        """
        Fetch Euribor rates data from an API.

        Returns:
            dict: A dictionary containing Euribor rates for different tenors.

        This function sends an API request to retrieve Euribor rates data and then extracts and organizes the rates
        for tenors of 3 months, 6 months, and 12 months into a dictionary. The function returns this dictionary.
        """
        url = "https://euribor.p.rapidapi.com/all"

        headers = {
            "X-RapidAPI-Key": "46bc3a6f18mshb2d07e9eb01ef29p1c2d78jsn578089492ef1",
            "X-RapidAPI-Host": "euribor.p.rapidapi.com"
        }

        EURIBOR = requests.get(url, headers=headers).json()

        euribor_rates = {
            '3months': EURIBOR['3months']/100,
            '6months': EURIBOR['6months']/100,
            '12months': EURIBOR['12months']/100
        }
        return euribor_rates

    def get_esterdata():
        API_KEY = 'Jcu52w5Gpb+4VrQI58md/A==lPpZWr0GtZ9GlZzg'
        api_url = 'https://api.api-ninjas.com/v1/interestrate'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY}).json()

        ester_rate_pct = None
        for item in response["non_central_bank_rates"]:
            if item["name"] == "ESTER":
                ester_rate_pct = item["rate_pct"]/100
        return ester_rate_pct
