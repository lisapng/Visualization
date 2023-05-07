#!/usr/bin/env python
# coding: utf-8

pip install pandas


# In[ ]:


import requests
from IPython.display import display, HTML
from ipywidgets import interact_manual
import json
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

def geocode(location):
    query_string = {'q' : location, 'format': 'json'}
    url = 'https://nominatim.openstreetmap.org/search'
    response = requests.get(url, params = query_string)
    response.raise_for_status()
    geodata = response.json()
    return geodata

def GetOffenders(lat, lon):
    apikey = '3CA27D62-D057-4D9B-BF1F-F22C2906FE51'
    lite = 0
    miles = 1
    type = 'searchbyspecificlatlong'
    url = 'https://services.familywatchdog.us/rest/json.asp?'
    query_string = {'key' : apikey, 'lite' : lite, 'type' : type, 'lat' : lat, 'long' : lon, 'miles' : miles }
    response = requests.get(url, params = query_string)
    response.raise_for_status()
    dataset = response.json()
    return dataset

fofo = GetOffenders(40.7127281, -74.0060152)

def write_json(data, filename):
    with open(filename, 'w') as f:
        file = json.dump(data, f, indent=4)
    return file

def getOffenderInfo(file):
    new_dict = []
    myjson = open(file, 'r')   #citation; recieved tons of guidance on extracting data from a json file here: https://www.youtube.com/watch?v=aj4L7U7alNU
    jsondata = myjson.read()
    obj = json.loads(jsondata)
    list= (obj['offenders'])
    for off in list:
        if off['convictions'] != []:
            off_charges = off['convictions'][0]['charge']
        else: 
            off_charges = []
        if off['markings'] != []:
            off_markings = off['markings'][0]['description']
        else:
            off_markings = []
        name = off['name']
        dob = off['dob']
        sex = off['sex']
        race = off['race']
        hair = off['hair']
        height = off['height']
        weight = off['weight']
        convictlevel = off['convictiontype']
        homeaddress = off['street1'], off['city'], off['state'], off['zipcode']
        photo = off['photo']
        latitude = off['latitude']
        longitude = off['longitude']
        new_dict.append({'name': name, 'DOB': dob, 'sex': sex, 'race': race, 'hair': hair, 'height': height, 'weight': weight, 'convictlevel': convictlevel, 'homeaddress': homeaddress,'charges': off_charges, 'markings': off_markings, 'photo': photo, 'latitude': latitude, 'longitude': longitude})
        with open('offenderinformation_data.json', 'w') as f:
            newfile = json.dump(new_dict, f, indent=4)
    return newfile

display(HTML('<h2>*** Run for a saved dataset of offenders within your city ***</h2>'))
@interact_manual(location="")
def GetLocation(location):
    loco = geocode(location)
    for coord in loco:
        lat = coord['lat']
        lon = coord['lon']
        fofo = GetOffenders(lat, lon)
        beo = write_json(fofo, 'original_offenders_dataset.json')
        ric = getOffenderInfo('original_offenders_dataset.json')
        return ric


# In[ ]:


import pandas as pd
# citation; recieved guidance on json pandas dataframe from https://www.youtube.com/watch?v=RRSJjxJhVEM&t=352s

off_file = 'offenderinformation_data.json'
with open(off_file) as f:
    data = json.load(f)
    
all_offenders = pd.DataFrame(columns=['Name', 'DOB', 'Sex', 'Race', 'Hair', 'Height', 'Weight', 'Conviction Level', 'Home Address', 'Charge(s)', 'Marking(s)', 'Photo', 'Latitude', 'Longitude'])

for i in range(0, len(data)):
    currentitem = data[i]
    all_offenders.loc[i] = [data[i]['name'], data[i]['DOB'], data[i]['sex'], data[i]['race'], data[i]['hair'], data[i]['height'], data[i]['weight'], data[i]['convictlevel'], data[i]['homeaddress'], data[i]['charges'], data[i]['markings'], data[i]['photo'], data[i]['latitude'], data[i]['longitude']]

display(HTML('<h2>************************************ A dataframe of each offender ************************************</h2>'))    
    
all_offenders       


# In[ ]:


all_offenders['SexCat'] = np.nan
    
all_offenders['SexCat'][ all_offenders['Sex'] == 'Male'] = 'Male'
all_offenders['SexCat'][ all_offenders['Sex'] == 'M'] = 'Male'
all_offenders['SexCat'][ all_offenders['Sex'] == 'MALE'] = 'Male'
all_offenders['SexCat'][ all_offenders['Sex'] == 'Female'] = 'Female'

all_offenders['SexCat'].value_counts()

risk1 = all_offenders[ all_offenders['Conviction Level'] == '1']
risk1['SexCat'].value_counts()

risk2 = all_offenders[ all_offenders['Conviction Level'] == '2']
risk2['SexCat'].value_counts()

risk3 = all_offenders[ all_offenders['Conviction Level'] == '3']
risk3['SexCat'].value_counts()

risk4 = all_offenders[ all_offenders['Conviction Level'] == '4']
risk4['SexCat'].value_counts()

sex_series = all_offenders['SexCat'].value_counts()
risk1_series = risk1['SexCat'].value_counts()
risk2_series = risk2['SexCat'].value_counts()
risk3_series = risk3['SexCat'].value_counts()
risk4_series = risk4['SexCat'].value_counts()

sex_df = pd.DataFrame( {'All' :sex_series, 'Risk Level 1' :risk1_series, 'Risk Level 2' :risk2_series,'Risk Level 3' :risk3_series,'Risk Level 4' :risk4_series})

display(HTML('<h2>***************** How do female and male offenders compare on their risk level? *****************</h2>'))

sex_df


# In[ ]:


all_offenders['RaceCat'] = np.nan
    
all_offenders['RaceCat'][ all_offenders['Race'] == 'White'] = 'White'
all_offenders['RaceCat'][ all_offenders['Race'] == 'W'] = 'White'
all_offenders['RaceCat'][ all_offenders['Race'] == 'Black'] = 'Black'
all_offenders['RaceCat'][ all_offenders['Race'] == 'Asian'] = 'Asian'

risk_1 = all_offenders[ all_offenders['Conviction Level'] == '1']
risk_1['RaceCat'].value_counts()

risk_2 = all_offenders[ all_offenders['Conviction Level'] == '2']
risk_2['RaceCat'].value_counts()

risk_3 = all_offenders[ all_offenders['Conviction Level'] == '3']
risk_3['RaceCat'].value_counts()

risk_4 = all_offenders[ all_offenders['Conviction Level'] == '4']
risk_4['RaceCat'].value_counts()

race_series = all_offenders['RaceCat'].value_counts()
risk1_seq = risk_1['RaceCat'].value_counts()
risk2_seq = risk_2['RaceCat'].value_counts()
risk3_seq = risk_3['RaceCat'].value_counts()
risk4_seq = risk_4['RaceCat'].value_counts()

race_df = pd.DataFrame( {'All' :race_series, 'Risk Level 1' :risk1_seq, 'Risk Level 2' :risk2_seq,'Risk Level 3' :risk3_seq,'Risk Level 4' :risk4_seq})

display(HTML('<h2>************* How does race/ethnic background come into play for conviction level? *************</h2>'))

race_df


# In[ ]:


import pandas as pd
import folium

#citation; recieved guidance with this part of the program from https://www.youtube.com/watch?v=FdqDgoG-SFM&t=891s

def set_marker_color(row):
    if row['Conviction Level'] == '1':
        return 'green'
    elif row['Conviction Level'] == '2':
        return 'blue'
    elif row['Conviction Level'] == '3':
        return 'pink'
    elif row['Conviction Level'] == '4':
        return 'purple'
    
all_offenders['color'] = all_offenders.apply(set_marker_color, axis=1)

CENTER_US = (39.8333333,-98.585522)
off_map = folium.Map(
    location=CENTER_US,
    zoom_start=4
)

for _, indiv in all_offenders.iterrows():
    folium.Marker(
        location=[indiv['Latitude'], indiv['Longitude']],
        popup=(indiv['Name'], indiv['Charge(s)'], indiv['Home Address']),
        tooltip=(indiv['Name'], indiv['Charge(s)'], indiv['Home Address']),
        icon=folium.Icon(color=indiv['color'], prefix='fa', icon='circle'),
    ).add_to(off_map)
    
    
display(HTML('<h2>**************************************** Offenders in your area ****************************************</h2>'))    
display(HTML('<body> Risk Level 1: green </body>'))
display(HTML('<body> Risk Level 2: blue </body>'))
display(HTML('<body> Risk Level 3: pink </body>'))
display(HTML('<body> Risk Level 4: purple </body>'))
            
    
off_map.save('nearest_offenders_in_the_area.html')

off_map


# In[ ]:




