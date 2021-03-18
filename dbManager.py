#!/usr/bin/env python3

# Autor: José Luis Martínez Cadavid <jlcadavid@uninorte.edu.co>

import psycopg2

# Función de inserción en la base de datos
def insert(table, columns, *args):
    sqlInsert = f"""INSERT INTO {table}({columns})
             VALUES {args}"""

    curDB = connDB.cursor()

    # execute the INSERT statement
    curDB.execute(sqlInsert)

    # close communication with the PostgreSQL database server
    curDB.close()
    # commit the changes
    connDB.commit()


# Función de inserción o actualización en la base de datos
def upsert(table, columns, *args):
    sqlUpsert = f"""INSERT INTO {table}({columns})
                VALUES {args}
                ON CONFLICT (user_ip)
                DO UPDATE
                SET calls_counter = {table}.calls_counter + 1
                """

    curDB = connDB.cursor()

    # execute the UPDATE statement
    curDB.execute(sqlUpsert)

    # close communication with the PostgreSQL database server
    curDB.close()
    # commit the changes
    connDB.commit()


# Función de valor máximo
def maxValue(table, column):
    sqlMax = f"""SELECT * FROM {table} WHERE {column} = (SELECT MAX({column}) FROM {table})"""

    curDB = connDB.cursor()

    # execute the MAX statement
    curDB.execute(sqlMax)

    # get query result
    result = curDB.fetchall()

    if len(result) != 0:
        maxCall = 0
        maxItem = None
        for item in result:
            if item[4] > maxCall:
                maxCall = item[4]
                maxItem = item

        # close communication with the PostgreSQL database server
        curDB.close()
        # commit the changes
        connDB.commit()

        return(f'La IP {maxItem[0]} de {maxItem[2]} ({maxItem[1]}) con {str(maxItem[4]) + " invocaciones" if maxItem[4] != 1 else str(maxItem[4]) + " invocación"} y {maxItem[3]} kms de distancia.')
    else:
        # close communication with the PostgreSQL database server
        curDB.close()
        # commit the changes
        connDB.commit()

        return('No disponible.')


# Función de valor mínimo
def minValue(table, column):
    sqlMin = f"""SELECT * FROM {table} WHERE {column} = (SELECT MIN({column}) FROM {table})"""

    curDB = connDB.cursor()

    # execute the MIN statement
    curDB.execute(sqlMin)

    # get query result
    result = curDB.fetchall()

    if len(result) != 0:
        maxCall = result[0][4]
        minItem = result[0]
        for item in result:
            if item[4] > maxCall:
                maxCall = item[4]
                minItem = item

        # close communication with the PostgreSQL database server
        curDB.close()
        # commit the changes
        connDB.commit()

        return(f'La IP {minItem[0]} de {minItem[2]} ({minItem[1]}) con {str(minItem[4]) + " invocaciones" if minItem[4] != 1 else str(minItem[4]) + " invocación"} y {minItem[3]} kms de distancia.')
    else:
        # close communication with the PostgreSQL database server
        curDB.close()
        # commit the changes
        connDB.commit()

        return('No disponible.')


# Función de búsqueda de keywords
def searchValue(table, column, keyword):
    sqlSearch = f"""SELECT * FROM {table} WHERE {column} ~* '{keyword}'"""

    curDB = connDB.cursor()

    # execute the MIN statement
    curDB.execute(sqlSearch)

    # get query result
    result = curDB.fetchall()

    # close communication with the PostgreSQL database server
    curDB.close()
    # commit the changes
    connDB.commit()

    return(result)


# Función de obtiene toda la información de una tabla
def allValues(table):
    sqlAll = f"""SELECT * FROM {table}"""

    curDB = connDB.cursor()

    # execute the MIN statement
    curDB.execute(sqlAll)

    # get query result
    result = curDB.fetchall()

    # close communication with the PostgreSQL database server
    curDB.close()
    # commit the changes
    connDB.commit()

    return(result)


# Función de creación de tablas en la base de datos
def createTables():
    sqlTables = (
        """
            CREATE TABLE IF NOT EXISTS data (
                user_ip VARCHAR(255) PRIMARY KEY,
                country_code VARCHAR(3) NOT NULL,
                country_name VARCHAR(255) NOT NULL,
                distance FLOAT NOT NULL,
                calls_counter INTEGER NOT NULL

            )
            """,
        """
            CREATE TABLE IF NOT EXISTS logs (
                log_id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                date_time VARCHAR(255) NOT NULL
            )
            """)

    curDB = connDB.cursor()

    # create table one by one
    for sql in sqlTables:
        try:
            curDB.execute(sql)
        except Exception as e:
            print(e)
            continue

    # close communication with the PostgreSQL database server
    curDB.close()
    # commit the changes
    connDB.commit()


# Función de desconexión de la base de datos
def disconnectDB():
    # close connection with the PostgreSQL database server if exists
    if connDB is not None:
        connDB.close()
    # print('Database connections closed.')


# Función de conexión a la base de datos
def connectDB():
    return psycopg2.connect(
        host='db', port='5432', database='data', user='postgres', password='07021997')


connDB = connectDB()
createTables()
