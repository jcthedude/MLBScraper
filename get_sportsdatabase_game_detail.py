import mysql.connector
from datetime import datetime
import urllib3
from bs4 import BeautifulSoup
from globals import *


def get_game_details():
    valid_url = True
    http = urllib3.PoolManager()

    # make sure http request is valid
    try:
        r = http.request('GET', sports_database_url)
    except:
        valid_url = False
        print("Problem with URL data returned.")
        pass

    # print details for console tracking
    print("URL: ", sports_database_url)

    # proceed with the process is there's a valid http response
    if valid_url:
        # soup the data returned from the http request
        soup = BeautifulSoup(r.data, 'html.parser')

        # setup soups
        try:
            soup_game_data = soup.find_all("table", {"id": "outer"})[0].find_all("table", {"id": "DT_Table"})[0].find_all('tr')
        except IndexError:
            soup_game_data = None
            print("Index error")
            pass

        # parse soups
        if soup_game_data is not None:
            count = 1
            for row in soup_game_data:
                print("Row count: ", count)
                for data in row.find_all('td'):
                    print(data.get_text().strip())
                count += 1
        else:
            print("No data found")


def db_read():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Raw_GameDetail""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    connection.close()


get_game_details()
