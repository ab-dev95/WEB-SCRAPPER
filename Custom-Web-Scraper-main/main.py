import requests
from bs4 import BeautifulSoup
import pandas as pd


list_name = []
list_score = []
list_title = []
list_value = []


response = requests.get(url='https://www.nba.com/stats')
response.raise_for_status()
web_text = response.text

soup = BeautifulSoup(web_text, 'html.parser')
# print(soup)
sections = soup.find_all('div', class_='LeaderBoardCard_lbcWrapper__e4bCZ')


for i in sections:
    try:
        list_title.append(i.select_one('.LeaderBoardCard_lbcTitle___WI9J').getText())
        data = i.select('.LeaderBoadTeamCard_lbtcTable__gmmZz tbody')
        data1 = i.select('.LeaderBoardPlayerCard_lbpcTable__q3iZD tbody')
    except AttributeError:
        pass
    else:
        for j in data:
            value_name = j.select('td a')
            value_score = j.select('.LeaderBoardWithButtons_lbwbCardValue__5LctQ')
            for name in value_name:
                list_name.append(name.getText())
            for score in value_score:
                list_score.append(score.getText())
        for k in data1:
            value_name1 = k.select('td a')
            for name1 in value_name1:
                list_value.append(name1.getText())
# print(list_title)
# print(list_value)
# print(list_name)
# print(list_score)


final_list = []
for i in list_title:
    for _ in range(5):
        final_list.append(i)
# print(final_list)

list_1 = list_value[::2]
list_2 = list_value[1::2]
# print(list_1)
# print(list_2)


player_data = {
    "Category": final_list[:45],
    "Player_Name": list_1,
    "Player_Score": list_2,
}
player_df = pd.DataFrame(player_data)
pd.options.display.max_columns = 4
# print(player_df) 

team_data = {
    "Category": final_list[45:],
    "Team": list_name,
    "Team_score": list_score,
}
team_df = pd.DataFrame(team_data)
print(team_df) 


player_df.to_csv('./data/player_data.csv')
team_df.to_csv('./data/team_data.csv')




