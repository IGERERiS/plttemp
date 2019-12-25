# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 16:39:25 2019

@author: eltsovt
"""
import pandas as pd
import plotly.express as px
import numpy as np

#word = input('Type the region please:')

#if len(word) < 1:
#    print('You should use one of the following enumeration values: world, usa, europe, asia, africa, north america, south america')
#    quit()
    
    
np.random.seed(1)

gapminder = px.data.gapminder().query("year == 2007")

file_inp=open('data_inp.txt', 'r').readlines()

country_dict = {}

dictionary = {}
keys = []

for line in file_inp:
    line = line.replace('\n', '')
    words = line.split('\t')
# We ignore first line    
#    words = words[1:]
    if keys == []:
        keys = words
    else:
        for i in range(len(words)):
            dictionary.setdefault(keys[i], []).append(words[i])

wide_df = pd.DataFrame(dictionary)
my_list = wide_df["publ_num_seg"].tolist()

for index, item in enumerate(my_list):
    my_list[index] = float(item)
    
#for element in my_list:
#    print(element, type(element))
    
#print(len(my_list))

gapminder = px.data.gapminder().query("year==2007")

#print(gapminder.index[gapminder.country == "Colombia"])

#count = 0
#for element in gapminder['country']:
#    for item in wide_df['country']:
#        if element == item:
#            count += 1
##            print(element, item)
            



#gapminder['publ_num_seg'] = pd.Series(abs(np.random.randn(len(gapminder["country"]))), index = gapminder.index)
gapminder['publ_num_seg'] = pd.Series(my_list, index = gapminder.index)

gapminder = gapminder.append({'country' : 'Russia' , 
                              'continent' : 'Europe', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'RUS', 
                              'iso_num' : 643,
                              'publ_num_seg' : 4.518798989} , ignore_index=True)

gapminder = gapminder.append({'country' : 'UAE' , 
                              'continent' : 'Asia', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'ARE', 
                              'iso_num' : 784,
                              'publ_num_seg' : 0.519616331} , ignore_index=True)

gapminder = gapminder.append({'country' : 'Uganda' , 
                              'continent' : 'Africa', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'UGA', 
                              'iso_num' : 800,
                              'publ_num_seg' : 0.022771307} , ignore_index=True)

gapminder = gapminder.append({'country' : 'Ukraine' , 
                              'continent' : 'Europe', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'UKR', 
                              'iso_num' : 804,
                              'publ_num_seg' : 0.291459396} , ignore_index=True)

gapminder = gapminder.append({'country' : 'Unknown Academia' , 
                              'continent' : 'Asia', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'ATA', 
                              'iso_num' : 10,
                              'publ_num_seg' : 0.979064732} , ignore_index=True)    

gapminder = gapminder.append({'country' : 'Azerbaijan' , 
                              'continent' : 'Asia', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'AZE', 
                              'iso_num' : 31,
                              'publ_num_seg' : 0.009857055} , ignore_index=True)   

gapminder = gapminder.append({'country' : 'Belarus' , 
                              'continent' : 'Europe', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'BLR', 
                              'iso_num' : 112,
                              'publ_num_seg' : 0} , ignore_index=True)   

gapminder = gapminder.append({'country' : 'Brunei' , 
                              'continent' : 'Asia', 
                              'year' : '2007', 
                              'lifeExp' : 100, 
                              'pop' : 100, 
                              'gdpPercap' : 100, 
                              'iso_alpha' : 'BRN', 
                              'iso_num' : 96,
                              'publ_num_seg' : 0.01854767} , ignore_index=True)           

gapminder = gapminder.append({'country' : 'Bulgaria' , 
                          'continent' : 'Europe', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'BGR', 
                          'iso_num' : 100,
                          'publ_num_seg' : 0.016707112} , ignore_index=True)           

gapminder = gapminder.append({'country' : 'Estonia' , 
                          'continent' : 'Europe', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'EST', 
                          'iso_num' : 233,
                          'publ_num_seg' : 0} , ignore_index=True)           
    
gapminder = gapminder.append({'country' : 'Hungary' , 
                          'continent' : 'Europe', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'HUN', 
                          'iso_num' : 348,
                          'publ_num_seg' : 0.05590874} , ignore_index=True)           
    
gapminder = gapminder.append({'country' : 'Kazahstan' , 
                          'continent' : 'Asia', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'KAZ', 
                          'iso_num' : 398,
                          'publ_num_seg' : 0.011505648} , ignore_index=True)           

gapminder = gapminder.append({'country' : 'Laos' , 
                          'continent' : 'Asia', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'LAO', 
                          'iso_num' : 418,
                          'publ_num_seg' : 0.007185838} , ignore_index=True)        

gapminder = gapminder.append({'country' : 'Latvia' , 
                          'continent' : 'Europe', 
                          'year' : '2007', 
                          'lifeExp' : 100, 
                          'pop' : 100, 
                          'gdpPercap' : 100, 
                          'iso_alpha' : 'LVA', 
                          'iso_num' : 428,
                          'publ_num_seg' : 0.022348866 } , ignore_index=True)       

gapminder = gapminder.append({'country' : 'Lithuania' , 
                      'continent' : 'Europe', 
                      'year' : '2007', 
                      'lifeExp' : 100, 
                      'pop' : 100, 
                      'gdpPercap' : 100, 
                      'iso_alpha' : 'LTU', 
                      'iso_num' : 440,
                      'publ_num_seg' : 0 } , ignore_index=True)       

gapminder = gapminder.append({'country' : 'Palestine' , 
                      'continent' : 'Asia', 
                      'year' : '2007', 
                      'lifeExp' : 100, 
                      'pop' : 100, 
                      'gdpPercap' : 100, 
                      'iso_alpha' : 'PSE', 
                      'iso_num' : 275,
                      'publ_num_seg' : 0 } , ignore_index=True)       


gapminder = gapminder.append({'country' : 'Qatar' , 
                      'continent' : 'Asia', 
                      'year' : '2007', 
                      'lifeExp' : 100, 
                      'pop' : 100, 
                      'gdpPercap' : 100, 
                      'iso_alpha' : 'QAT', 
                      'iso_num' : 634,
                      'publ_num_seg' : 0.015059281 } , ignore_index=True)       

gapminder = gapminder.append({'country' : 'Republic of Malta' , 
                      'continent' : 'Europe', 
                      'year' : '2007', 
                      'lifeExp' : 100, 
                      'pop' : 100, 
                      'gdpPercap' : 100, 
                      'iso_alpha' : 'MLT', 
                      'iso_num' : 470,
                      'publ_num_seg' : 0.007569732 } , ignore_index=True)       
        
#gapminder = gapminder.append({'country' : 'Republic of South Africa' , 
#                      'continent' : 'Africa', 
#                      'year' : '2007', 
#                      'lifeExp' : 100, 
#                      'pop' : 100, 
#                      'gdpPercap' : 100, 
#                      'iso_alpha' : 'ZAF', 
#                      'iso_num' : 710,
#                      'publ_num_seg' : 0.645627297 } , ignore_index=True) 
rsa = input('vvedite rosf')
rsa = eval(rsa)
#gapminder = gapminder.append({'country' : 'Republic of South Africa' , 'continent' : 'Africa', 'year' : '2007', 'lifeExp' : 100, 'pop' : 100,'gdpPercap' : 100,  'iso_alpha' : 'ZAF', 'iso_num' : 710, 'publ_num_seg' : 0.645627297 } , ignore_index=True) 

gapminder = gapminder.append(rsa, ignore_index=True)

#{'country' : 'Republic of South Africa' , 'continent' : 'Africa', 'year' : '2007', 'lifeExp' : 100, 'pop' : 100,'gdpPercap' : 100,  'iso_alpha' : 'ZAF', 'iso_num' : 710, 'publ_num_seg' : 0.645627297 } , ignore_index=True

#print(gapminder)
#
#print("=======================================================================")
#print(gapminder)
#print("=======================================================================")
#formatted_df = pd.melt(df,
#                       ["religion"],
#                       var_name="income",
#                       value_name="freq"


#fig = px.bar(tidy_df, x="Month", y="value", color="variable", barmode="group")

fig = px.scatter_geo(gapminder, locations="iso_alpha",
                     color='iso_alpha', # which column to use to set the color of markers
#                     hover_name="country", # column added to hover information
                     size="publ_num_seg",            # size of markers
                     size_max=50,
#                     projection="natural earth",

                     )

fig.update_layout(             # all "layout" attributes: /python/reference/#layout
#    title="Easy to plot",

      geo = dict(
#       scope='north america',
#        scope='europe',
#        scope='south america',
#        scope='africa',     
#        scope='asia',        
#        scope=world,        
            resolution = 110,
#            projection=dict( type='mercator' ),
        showland = True,
#            landcolor = "rgb(217, 217, 217)",
#            subunitcolor="rgb(255, 255, 255)",
#            countrycolor="rgb(255, 255, 255)",
#            lonaxis = dict( range= [ 14.0, 24.0 ] ),
#            lataxis = dict( range= [ 49.0, 55.0 ] ),            
        showcountries = True,
        countrywidth = 0.2,
        coastlinewidth = 0.5,
        
    ),  
 
    showlegend=False,
  
#    annotations=[
#        dict(                            # all "annotation" attributes: /python/reference/#layout-annotations
#            text="annotation",    # /python/reference/#layout-annotations-text
#            x=0.1,                         # /python/reference/#layout-annotations-x
#            xref="paper",                # /python/reference/#layout-annotations-xref
#            y=0.1,                         # /python/reference/#layout-annotations-y
#            yref="paper"                 # /python/reference/#layout-annotations-yref
#        )
#    ] 
    
    )

  
#fig.write_image('C:\\temp\\Tex\\MDPI_SEG\\images\\fig1.svg')  


#fig.savefig('C:\\temp\\Tex\\MDPI_SEG\\images\\'+'word'+'.png', dpi=300)
fig.show()