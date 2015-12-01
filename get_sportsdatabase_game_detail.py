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
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            count = 1

            # get row data
            for row in soup_game_data:
                row_list = []
                for data in row.find_all('td'):
                    row_list.append(data.get_text().strip())

                if len(row_list) != 0:
                    # convert date
                    row_list[1] = str(datetime.strptime(row_list[1], '%Y%m%d').date())

                    # check for null values in rest columns
                    if row_list[12] == '-':
                        row_list[12] = 0
                    if row_list[16] == '-':
                        row_list[16] = 0
                    if row_list[17] == '-':
                        row_list[17] = 0
                    if row_list[18] == '-':
                        row_list[18] = 0
                    if row_list[25] == '-':
                        row_list[25] = 0
                    if row_list[29] == '-':
                        row_list[29] = 0
                    if row_list[30] == '-':
                        row_list[30] = 0
                    if row_list[31] == '-':
                        row_list[31] = 0
                    if row_list[32] == '-':
                        row_list[32] = 0
                    if row_list[35] == '-':
                        row_list[35] = 0

                    # insert row into db
                    db_insert(cursor, row_list, count)

                    count += 1

            connection.commit()
            connection.close()
        else:
            print("No data found")

    return count


def db_truncate():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM Raw_GameDetail""")
    connection.commit()
    connection.close()

    print("Table truncated.")


def db_insert(cursor, row_list, count):
    print("Row #: ", count, " ---- ", row_list)

    cursor.execute("""INSERT INTO Raw_GameDetail (Season, Date ,Day, GameNumber, SeriesGame, Margin, HomeTeam, HomeRuns, HomeWins, HomeLosses, HomeStreak, HomeMatchupWins, HomeRest
        , HomeSiteStreak, HomeStarterWins, HomeStarterLosses, HomeStarterRest, HomeLine, HomeProfit, AwayTeam, AwayRuns, AwayWins, AwayLosses, AwayStreak, AwayMatchupWins, AwayRest
        , AwaySiteStreak, AwayStarterWins, AwayStarterLosses, AwayStarterRest, AwayLine, AwayProfit, OUMargin, Over, Under, OUStreak) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        , (row_list[0], row_list[1], row_list[2], row_list[3], row_list[4], row_list[5], row_list[6], row_list[7], row_list[8], row_list[9], row_list[10], row_list[11], row_list[12]
        , row_list[13], row_list[14], row_list[15], row_list[16], row_list[17], row_list[18], row_list[19], row_list[20], row_list[21], row_list[22], row_list[23], row_list[24]
        , row_list[25], row_list[26], row_list[27], row_list[28], row_list[29], row_list[30], row_list[31], row_list[32], row_list[33], row_list[34], row_list[35]))


def db_select():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Raw_GameDetail""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    connection.close()


def main():
    start_time = datetime.now()
    print("Start time: ", str(start_time))

    db_truncate()

    count = get_game_details()

    # print process results
    print("Process complete. ", count, "rows processed.")
    end_time = datetime.now()
    duration = end_time - start_time
    print("Start time: ", str(start_time))
    print("End time: ", str(end_time))
    print("Total duration (minutes): ", str(duration.seconds / 60))


main()
