'''
def main():
    '''My Climbing App'''
    
    st.title('Hello World')
    
if __name__ == '__main__':
    main()
'''

import streamlit as st
import numpy as np
import pandas as pd
import csv
import datetime

st.title('Best Climbing Cities')

df = pd.DataFrame({
  'Available Grades': ['5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13','5.14'],
})

st.sidebar.markdown('Available Options')

lg = st.sidebar.selectbox(
    'What is your favorite grade?',
     df['Available Grades'])

style = st.sidebar.selectbox(
    'What style do you prefer?',
     ['Trad','Sport','TR'])

# hg = st.selectbox(
  #  'What is the highest grade?',
  #   df['Available Grades'])

criteria = st.sidebar.selectbox(
    'What criteria do you want to use?',
     ['Most Routes','Most Votes','Average Star Rating'])

feedback = st.sidebar.text_area('What new features would you like to see?')
press=st.sidebar.button('Submit')

if press: 
    with open('feedback.csv', 'a',newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow([feedback,datetime.datetime.now()])

#st.sidebar.markdown('The current text is '+feedback)

cities= [['NewYork',40.66,-73.93,1,1,1,1],
    ['LosAngeles',34.02,-118.41,1,1,1,1],
    ['Phoenix',33.57,-112.09,1,1,1,1],
    ['SanDiego',32.81,-117.13,1,1,1,1],
    ['Austin',30.30,-97.75,1,1,1,1],
    ['SanFrancisco',37.73,-123.03,1,1,1,1],
    ['Seattle',47.62,-122.35,1,1,1,1],
    ['Denver',39.76,-104.88,1,1,1,1],
    ['Boston',42.33,-71.02,1,1,1,1],
    ['ElPaso',31.84,-106.42,1,1,1,1],
    ['Nashville',36.17,-86.78,1,1,1,1],
    ['Portland',45.53,-122.65,1,1,1,1],
    ['LasVegas',36.23,-115.26,1,1,1,1],
    ['SaltLakeCity',40.77,-111.93,1,1,1,1]]

for x in range(len(cities)):
    file = 'merged_file_'+cities[x][0]+'.json'
    df2 = pd.read_json(file)
    cities[x][3] = df2[(df2['type'].str.contains(style)) & (df2['rating'].str.contains(lg))].count()['id']
    cities[x][4] = df2[(df2['type'].str.contains(style)) & (df2['rating'].str.contains(lg))].mean()['stars']
    cities[x][5] = df2[(df2['type'].str.contains(style)) & (df2['rating'].str.contains(lg))].sum()['starVotes']

map_data = pd.DataFrame(
    cities,columns = ['City','lat', 'lon','Routes','Mean Star Rating','Votes','rad'])

citiespd = map_data.drop(columns=['lat', 'lon','rad'])

if criteria == 'Most Routes':
    crit = 'Routes'
elif criteria == 'Most Votes':
    crit = 'Votes'
elif criteria == 'Average Star Rating':
    crit = 'Mean Star Rating'

citiespd.sort_values(by=[crit], inplace=True, ascending=False)    
scale_radius=250000/citiespd[crit].max()

st.deck_gl_chart(
    viewport={
        'latitude': 39.20,
        'longitude': -96.58,
        'zoom': 3,
        # 'pitch': 50,
        },
    layers=[
        {
            'type': 'ScatterplotLayer',
            'data': map_data,
            'getRadius': crit,
            'radiusScale': scale_radius,
        },
        {
            'type': 'TextLayer',
            'data': map_data,
            'getText': 'City',
            'getColor': [0, 0, 0, 200],
            'getSize': 20,
        }])

st.write('*Based on a 150 mile radius')

if st.checkbox('Show raw data'):
    #citiespd.style.hide_columns(['lat','lon']).hide_index()
    st.dataframe(citiespd.style.highlight_max(axis=0)\
                 .set_precision(3))