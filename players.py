import requests
import pandas as pd
import streamlit as st
import sys
from bs4 import BeautifulSoup


# project name
st.markdown('<h1 style="padding: 20px; text-align: center">🏏CRICKET.IO</h1>',unsafe_allow_html=True)

# funtion to read css file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# creating search bar 
selected = st.text_input("Enter Player Name:", "Search..")
# creating button
button_clicked = st.button("OK")

# spliting player name
name = selected.split()
# joining player name ex:- user enters virat kohli formated_name:- virat-kohli
formated_name = "-".join(name)


if button_clicked:
  
    url = f"https://www.sportskeeda.com/player/{formated_name}"
     
    res = requests.get(url)
      
    if res.status_code == 404:
        st.error("Please check player name...  Error: 404")
        sys.exit()
    else:
        soup = BeautifulSoup(res.content, 'html.parser')

        player_image = soup.find('div',{"class":"player-img"})
        src = player_image.find('img').attrs['src']
        st.markdown(f'<img style="height:190px;margin:0px 0px 0px 0px;border-radius:100px;padding:10px;background:#e8e8e8;width: 190px;object-fit:cover;object-position: top;" src="{src}" />',unsafe_allow_html=True)

        # It will give full Name born height nationality role relations
        fields = soup.find_all('td', class_='left')
        # It will return file_values
        field_values = soup.find_all('td', class_='right')

        # It will return length of fields
        length = len(fields)
            
        # player name    
        st.markdown(f"<h1>{field_values[0].text}</h1>", unsafe_allow_html=True)

        for i in range(1,length):
            st.code(f"{fields[i].text} :- {field_values[i].text}")

            
    # Batting stats
        
        # Selecting all section tag in which all data is present
        section = soup.find_all('section',class_="cricket-stats")
        # section[1] contains all batting stats data
        batting_stats = section[1]
        # section[1] contains 'th' tag
        batting_titles = batting_stats.find_all('th')
        # batting_titles is list of titles: Game-Type,INN, Runs, 4s , 6s etc
        length_bat = len(batting_titles)
        
        # finding 'tr' tag in section[1]
        bat_matchs = batting_stats.find_all('tr') 
        
        # finding al 'td' tag which is inside 'tr' tag for actual data of runs, 4s, 6s 
        try:
            odis_ele = bat_matchs[1].find_all('td')
            tests_ele = bat_matchs[2].find_all('td')
            t20s_ele = bat_matchs[4].find_all('td')
            listas_ele = bat_matchs[5].find_all('td')
            firstclass_ele = bat_matchs[6].find_all('td')
        except:
            st.success("Data not present")
        
        # creating empty list for all different types of matchs to store titles and its values
        odis_files = []
        tests_files = []
        t20s_files = []
        listas_files = []
        firstclass_files = []

        # for loop for inserting data in above empty list
        for i in range(1,length_bat):
            bat_title = batting_titles[i].text

            odis_score = odis_ele[i].text
            tests_score = tests_ele[i].text
            t20s_score = t20s_ele[i].text
            listas_score = listas_ele[i].text
            firstclass_score = firstclass_ele[i].text

            odis_files.append(
                [bat_title,odis_score]
            ) 
            tests_files.append(
                [bat_title,tests_score]
            )
            t20s_files.append(
                [bat_title,t20s_score]
            )
            listas_files.append(
                [bat_title,listas_score]
            )
            firstclass_files.append(
                [bat_title,firstclass_score]
            )

        # 2 tuples for creating file name and match name we will use this as arguments while calling create_graph funtion
        files_list = ('odis_files','tests_files','t20s_files','listas_files','firstclass_files')
        match_ele_list = (odis_ele[0],tests_ele[0],t20s_ele[0],listas_ele[0],firstclass_ele[0])

        st.markdown(f'<h2 style="padding-top: 50px; text-align: center; color: green">Batting Stats</h2>',unsafe_allow_html=True)

        # funtion to convert list into dataFrame than converting to csv file and ploting graph 
        def create_graph(filename,matchname):

            # converting list into DataFrame
            df = pd.DataFrame(eval(filename))
            # converting DataFrame into csv file 
            df.to_csv(f'{matchname}.csv',index=False, header=['Game-Type','Score'], encoding='cp1252')
            # reading csv file
            data = pd.read_csv(f'{matchname}.csv')
            # seting index of graph
            data = data.set_index('Game-Type')
            st.markdown(f'<h3>{matchname}</h3>',unsafe_allow_html=True)
            # ploting bar graph using streamlit library
            st.bar_chart(data)

        # calling create_graph funtion in loop to plot n graph
        for i in range(0,len(files_list)): 
            # passing files_list and match_ele_list elements as arguments
            create_graph(files_list[i],match_ele_list[i].text)


        # Bowling Stats

        bowling_stats = section[2]
        bowling_titles = bowling_stats.find_all('th')
        length_bow = len(bowling_titles)

        bow_matchs = batting_stats.find_all('tr') 

        bow_odis_ele = bow_matchs[1].find_all('td')
        bow_tests_ele = bow_matchs[2].find_all('td')
        bow_t20s_ele = bow_matchs[4].find_all('td')
        bow_listas_ele = bow_matchs[5].find_all('td')
        bow_firstclass_ele = bow_matchs[6].find_all('td')

        bow_odis_files = []
        bow_tests_files = []
        bow_t20s_files = []
        bow_listas_files = []
        bow_firstclass_files = []


        for i in range(1,length_bow):
            bow_title = bowling_titles[i].text

            bow_odis_score = bow_odis_ele[i].text
            bow_tests_score = bow_tests_ele[i].text
            bow_t20s_score = bow_t20s_ele[i].text
            bow_listas_score = bow_listas_ele[i].text
            bow_firstclass_score = bow_firstclass_ele[i].text

            bow_odis_files.append(
                [bow_title,bow_odis_score]
            ) 
            bow_tests_files.append(
                [bow_title,bow_tests_score]
            )
            bow_t20s_files.append(
                [bow_title,bow_t20s_score]
            )
            bow_listas_files.append(
                [bow_title,bow_listas_score]
            )
            bow_firstclass_files.append(
                [bow_title,bow_firstclass_score]
            )

        bow_files_list = ('bow_odis_files','bow_tests_files','bow_t20s_files','bow_listas_files','bow_firstclass_files')
        bow_match_ele_list = (bow_odis_ele[0],bow_tests_ele[0],bow_t20s_ele[0],bow_listas_ele[0],bow_firstclass_ele[0])

        st.markdown(f'<h2 style="padding-top: 50px; text-align: center; color: green">Bowling Stats</h2>',unsafe_allow_html=True)

        def create_graph2(filename,matchname):
            df2 = pd.DataFrame(eval(filename)) 
            df2.to_csv(f'{matchname}_bow.csv',index=False, header=['Game-Type','Score'], encoding='cp1252')
            data2 = pd.read_csv(f'{matchname}_bow.csv')
            data2 = data2.set_index('Game-Type')
            st.bar_chart(data2)

        for i in range(0,len(bow_files_list)): 
            create_graph(bow_files_list[i],bow_match_ele_list[i].text)