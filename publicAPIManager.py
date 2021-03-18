#!/usr/bin/env python3

# Autor: José Luis Martínez Cadavid <jlcadavid@uninorte.edu.co>

import json
import requests

# Direcciones de APIs Públicas
IP2CountryBaseURL = 'https://api.ip2country.info/ip?'
RESTCountriesBaseURL = 'https://restcountries.eu/rest/v2/alpha/'

# Función de petición a API de IP2Country con número de IP.
def ip2Countrify(IP):

    api_url = IP2CountryBaseURL + IP

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


# Función de petición a API de RestCountries con ISO Code.
def restCountrify(countryCode):

    api_url = RESTCountriesBaseURL + countryCode.lower()

    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None