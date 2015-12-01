db_config = {
  'user': 'slampana',
  'password': 'Campana1',
  'host': '45.55.23.232',
  'database': 'mlb',
  'raise_on_warnings': True,
}

get_season = '2015'

sports_database_url = 'http://api.sportsdatabase.com/mlb/query?output=default&sdql=season%2C+date%2C+day%2C+game+number%2C+series+game%2C+margin%2C+team%2C+runs%2C+wins%2C+losses%2C+streak%2C+matchup+wins%2C+rest%2C+site+streak%2C+starter+wins%2C+starter+losses%2C+starter+rest%2C+line%2C+profit%2C+o%3Ateam%2C+o%3Aruns%2C+o%3Awins%2C+o%3Alosses%2C+o%3Astreak%2C+matchup+losses%2C+o%3Arest%2C+o%3Asite+streak%2C+o%3Astarter+wins%2C+o%3Astarter+losses%2C+o%3Astarter+rest%2C+o%3Aline%2C+o%3Aprofit%2C+ou+margin%2C+over%2C+under%2C+ou+streak+%40+season%3D'\
                      + get_season + '+and+site%3Dhome&submit=++S+D+Q+L+%21++'
