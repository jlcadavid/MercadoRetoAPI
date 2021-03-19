# MercadoRetoAPI
 IDM Challange 2020 - MELI
 
 INSTRUCCIONES DE EJECUCIÓN DE LA API:

    * EN WINDOWS:
        1. Descargar e instalar Docker:
            - https://hub.docker.com/editions/community/docker-ce-desktop-windows/

        2. Ejecutar "startAPI.bat" (se sugiere como Administrador).

        3. Realizar peticiones GET con Postman (https://www.postman.com/downloads/) o aplicación de preferencia una vez la API de MercadoReto haya iniciado.


    * EN MAC o LINUX:
        1. Descargar e instalar Docker:
            - En Mac: https://hub.docker.com/editions/community/docker-ce-desktop-mac/
            - En Linux: Seguir instrucciones de instalación según distribución de Linux para Docker y Docker Compose
                (https://docs.docker.com/engine/install/)

        2. Ejecutar "startAPI.sh" (brindar permisos de ejecución en Terminal con el comando => chmod +x startAPI.sh)

        3. Realizar peticiones GET con Postman (https://www.postman.com/downloads/) o aplicación de preferencia una vez la API de MercadoReto haya iniciado.


LINKS DE LA API:

    * GET http://localhost:5000?ip={IP_DE_USUARIO}

    * GET http://localhost:5000/countries?cc={ISO_CODE}


EJEMPLO DE USO DE LA API:

    * GET http://localhost:5000?ip=3.7.9.1
        - "response": {
                "Dirección IP": "3.7.9.1",
                "Fecha actual": "2021-03-12 17:37:25.931293",
                "País": "United States",
                "ISO Code": "US",
                "Distancia estimada": "8671.073208947953 kms",
                "Pertenece a AWS": "1 prefixes matching / 4081 prefixes found - (3.6.0.0/15 ap-south-1 AMAZON EC2)"
            }

    * GET http://localhost:5000/countries?cc=US
        - "response": {
                "Consulta más lejana de BS. AS.": "La IP 83.44.196.93 de Spain (ES) con 1 invocación y 10252.028809319725 kms de distancia.",
                "Consulta más cercana de BS. AS.": "La IP 3.7.9.1 de United States (US) con 2 invocaciones y 8671.073208947953 kms de distancia.",
                "Número de invocaciones promedio en United States (US)": 2.0
            }
