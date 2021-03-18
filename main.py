#!/usr/bin/env python3

# Realiza consultas rápidas de la información de cualquier dirección IP.
# Determina cuales tienen mayor o menor actividad y su promedio por país.
# Ej: investigar la dirección IP 83.44.196.93 de España (ES)
#   o ¿cuál es el promedio de invocaciones en Japón (JP)?

# Autor: José Luis Martínez Cadavid <jlcadavid@uninorte.edu.co>

from geopy import distance
from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import ipaddress
import json
import uuid
import jwt

import utils
import dbManager as db
import publicAPIManager as publicAPI
import awsIPSearch as ipSearch

# Latitud y Longitud de Buenos Aires, Argentina
BuenosAiresLatLng = [-34.0, -64.0]

# End-Point de Consultas de Direcciones IP
class UsersInfo(Resource):
    def get(self):
        try:
            accessDate = datetime.utcnow()
            userIP = format(ipaddress.ip_address(
                request.args.get('ip')))

            ip2CountryResponse = publicAPI.ip2Countrify(userIP)
            restCountriesResponse = publicAPI.restCountrify(
                ip2CountryResponse['countryCode'])

            est_distance = None
            if restCountriesResponse != None:
                est_distance = distance.distance((BuenosAiresLatLng[0], BuenosAiresLatLng[1]),
                                                 (restCountriesResponse['latlng'][0], restCountriesResponse['latlng'][1])).km

                db.upsert('data', 'user_ip, country_code, country_name, distance, calls_counter',
                          str(f'{userIP}'), str(ip2CountryResponse['countryCode']), str(f'{ip2CountryResponse["countryName"]}'), float(f'{est_distance}'), 1)

            return {
                'response': {
                    'Dirección IP': userIP,
                    'Fecha actual': json.dumps(accessDate, default=str).replace('\"', ''),
                    'País': ip2CountryResponse['countryName'] if len(ip2CountryResponse['countryName']) != 0 else 'No disponible.',
                    'ISO Code': ip2CountryResponse['countryCode'] if len(ip2CountryResponse['countryCode']) != 0 else 'No disponible.',
                    'Distancia estimada': f'{str(est_distance) + " kms" if est_distance != None else "No disponible"}',
                    'Pertenece a AWS': ipSearch.ip_lookup(True, userIP),
                }
            }, 200

        except ValueError:
            return{
                'error': 'La dirección IP digitada es inválida. Por favor, verifica e intenta de nuevo.'
            }, 500

    pass


# End-Point de Consultas de Información por Paises
class CountriesInfo(Resource):
    def get(self):
        accessDate = datetime.utcnow()
        userID = request.headers.get('User-ID') if request.headers.get(
            'User-ID') is not None else request.headers.get('User-Agent')

        db.insert('logs', 'user_id, date_time', userID, json.dumps(
            accessDate, default=str).replace('\"', ''))

        cc = format(request.args.get('cc'))

        if len(cc) > 1 and len(cc) <= 3:
            searchResult = db.searchValue('data', 'country_code', cc)
            if len(searchResult) != 0:
                callsMean = 0
                for item in searchResult:
                    callsMean = callsMean + item[4]
                callsMean = callsMean / len(searchResult)

                return {
                    'response': {
                        'Consulta más lejana de BS. AS.': db.maxValue('data', 'distance'),
                        'Consulta más cercana de BS. AS.': db.minValue('data', 'distance'),
                        f'Número de invocaciones promedio en {searchResult[0][2]} ({cc.upper()})': callsMean
                    }
                }, 200
            else:
                return {
                    'response': {
                        'Consulta más lejana de BS. AS.': db.maxValue('data', 'distance'),
                        'Consulta más cercana de BS. AS.': db.minValue('data', 'distance'),
                        'No se encontraron resultados para el ISO Code': cc.upper()
                    }
                }, 200
        else:
            return {
                'error': 'El ISO Code digitado es inválido. Verifica e intenta de nuevo.'
            }, 500

    pass


# Inicialización de API
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'

api = Api(app)

# Asignación de recursos de API
# '/' es el punto de entrada para la información de usuarios con la query '?ip={IP_DE_USUARIO}'.
api.add_resource(UsersInfo, '/')

# '/countries' es el punto de entrada para la información de paises con la query '?cc={ISO_CODE}'.
api.add_resource(CountriesInfo, '/countries')

if __name__ == '__main__':
    try:
        app.run(host='api', port='5000')
    finally:
        db.disconnectDB()
