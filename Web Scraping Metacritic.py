# This Script depicts my algorithm used to scrap video games data on MetaCritic. The aim was to structure data in a pandas data frame. I wish to improve
# this algorithm by going through many pages. My main goal is to investigate features of video games (license, developper, plateform) to predict a success
# through a classification tree. This will come later.

# Package Importation
from urllib import response
from bs4 import BeautifulSoup
import pandas as pd
import requests

#Initialization
user_agent = {'User-agent': 'Mozilla/5.0'} # In order to no be detected as a bot (important)
url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered"
response= requests.get(url, headers= user_agent)
response.status_code # check if scraping is allowed: It should be 200

#Parser of html file
soup = BeautifulSoup(response.text, 'html.parser') #On parse le code html selon les sélécteurs CSS
content = soup.find_all('td', class_ = 'clamp-summary-wrap') #On sélectionne la liste sous forme de tableau

#Collect information based on selector CSS
Jeux, Plateforme, Score, Date = [], [], [], []


for game in content:
    Jeux.append(game.find('h3').text)
    Plateforme.append(game.find('span', class_ = 'data').text)
    Date.append(game.find('div', class_ = 'clamp-details').text)
    Score.append(game.find('div', class_= 'metascore_w large game positive').text)
game_df = pd.DataFrame({'Name' : Jeux, 'Plateform': Plateforme, 'Date_release':Date, 'Score' : Score})

game_df.columns
