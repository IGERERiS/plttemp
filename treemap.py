import matplotlib.pyplot as plt
import matplotlib.cm as cm
import squarify # pip install squarify (algorithm for treemap)
import itertools
import collections
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import sqlite3
import time
import ssl
import ast
import random
# aver_coauth_numb_SEG - Average number of authors per paper (SEG Annual meetings). 1982-2019, 38 years in total
aver_coauth_numb_SEG = [2.1589403973509933, 2.1052631578947367, 1.9828009828009827, 2.2161383285302594, 2.058219178082192, 2.148014440433213, 2.1649484536082473, 2.313131313131313, 2.3133462282398454, 2.2195121951219514, 2.2872062663185377, 2.355, 2.504291845493562, 2.6057906458797326, 2.6205128205128205, 2.669741697416974, 2.734061930783242, 2.837638376383764, 2.908805031446541, 2.8248175182481754, 2.9011164274322168, 3.103448275862069, 3.0693815987933637, 3.127565982404692, 3.1204481792717087, 3.126782884310618, 3.3454790823211877, 3.2354948805460753, 3.308132875143184, 3.44815668202765, 3.552836484983315, 3.433628318584071, 3.494959677419355, 3.571296296296296, 3.476449275362319, 3.6575342465753424, 3.6621743036837375, 3.9009259259259259259259259259259]
# aver_coauth_numb_EAGE - Average number of authors per paper (EAGE Annual meetings). 2001-2019, 19 years in total
aver_coauth_numb_EAGE = [3.05, 3.0676258992805754, 2.979466119096509, 3.1364341085271317, 3.152269399707174, 3.044776119402985, 3.117283950617284, 3.2708978328173375, 3.2417127071823204, 3.3980044345898004, 3.1833872707659117, 3.227355072463768, 3.4643714971977584, 3.646404109589041, 3.7708333333333335, 3.671511627906977, 3.599670510708402, 3.6703577512776833, 3.9076923076923076]
# The reference data from Earht and planetary science
ref_data = [2.285361,2.269854,2.285205,2.274893, 2.32184, 2.352931, 2.433209, 2.402235, 2.433422, 2.49702, 2.594231, 2.581554, 2.727233, 2.789873, 2.874077, 2.885946, 3.018021, 3.166208, 3.372227, 3.288681, 3.346355, 3.463061, 3.437281, 3.519684, 3.67232, 3.747994, 3.896395, 3.848252, 4.055962, 4.122729, 4.207524, 4.246959, 4.315808, 4.348695, 4.480921, 4.601956, 4.730707]
end_year = 2019
european_countries = ['Albania', 'Republic of Albania', 'Andorra', 'Principality of Andorra', 'Austria', 'Republic of Austria', 'Belarus', 'Republic of Belarus', 'Belgium', 'Kingdom of Belgium', 'Bosnia and Herzegovina', 'Bosnia and Herzegovina', 'Bulgaria', 'Republic of Bulgaria', 'Croatia', 'Republic of Croatia', 'Czechia', 'Czech Republic', 'Czech Republic', 'Denmark', 'Kingdom of Denmark', 'Estonia', 'Republic of Estonia', 'Finland', 'Republic of Finland', 'France', 'French Republic', 'Germany', 'Federal Republic of Germany', 'Greece', 'Hellenic Republic', 'Holy See', 'Holy See', 'Hungary', 'Hungary', 'Iceland', 'Republic of Iceland', 'Ireland', 'Ireland', 'Italy', 'Republic of Italy', 'Latvia', 'Republic of Latvia', 'Liechtenstein', 'Liechtenstein', 'Lithuania', 'Republic of Lithuania', 'Luxembourg', 'Grand Duchy of Luxembourg', 'Malta', 'Republic of Malta', 'Moldova', 'Republic of Moldova', 'Monaco', 'Principality of Monaco', 'Montenegro', 'Montenegro', 'Netherlands', 'Kingdom of the Netherlands', 'North Macedonia', 'Republic of North Macedonia', 'Norway', 'Kingdom of Norway', 'Poland', 'Republic of Poland', 'Portugal', 'Portuguese Republic', 'Romania', 'Romania', 'Russia', 'Russian Federation', 'San Marino', 'Republic of San Marino', 'Serbia', 'Republic of Serbia', 'Slovakia', 'Slovak Republic', 'Slovenia', 'Republic of Slovenia', 'Spain', 'Kingdom of Spain', 'Sweden', 'Kingdom of Sweden', 'Switzerland', 'Swiss Confederation', 'Turkey', 'Republic of Turkey', 'Ukraine', 'Ukraine', 'United Kingdom', 'United Kingdom of Great Britain and Nothern Ireland']

all_countries = ['Albania', 'Algeria', 'Argentina', 'Australia', 'Austria', 'Azerbaijan', 'Bangladesh', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Cameroon', 'Canada', 'Chile', 'China', 'Colombia', 'Croatia', 'Czechia', 'Denmark', 'Djibouti', 'Dominican Republic', 'Egypt', 'Estonia', 'Ethiopia', 'Finland', 'France', 'Germany', 'Ghana', 'Greece', 'Haiti', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, Republic of', 'Kuwait', 'Lao People\'s Democratic Republic', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Lybia', 'Malaysia', 'Malta', 'Mexico', 'Mongolia', 'Morocco', 'Namibia', 'Netherlands', 'New Zealand', 'Nigeria', 'Norway', 'Oman', 'Pakistan', 'Palestine, State of', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russian Federation', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'South Africa', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Trinidad and Tabago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom of Great Britain and Nothern Ireland', 'United States of America', 'Unknown academia', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Yemen']

# The procedure to make list of zeros
def zerolistmaker(norm_basis):
    listofzeros = [0] * len(norm_basis)
    return listofzeros
# The procedure to convert strings to floats
def make_float(my_list):
    outputlist = []
    for item in my_list:
        if outputlist is []:
            outputlist[0] = float(item)
        else:
            outputlist.append(float(item))
    return outputlist

norm_basis = aver_coauth_numb_EAGE[5:]
conn = sqlite3.connect('Industry.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Industry")
data=cursor.fetchall()

printing_all = {}
# print(type(data))
ind_dict = {}
for element in data:
    ind_dict[element[0]] = ast.literal_eval(element[1])

conn_annual = sqlite3.connect('EAGE_affiliations_data.sqlite')
cursor_annual = conn_annual.cursor()
cursor_annual.execute("SELECT * FROM EAGE_affiliations_data")
data_read=cursor_annual.fetchall()
# print(data_read)
occurrences_dict = {}

for element in data_read:
    if element[0] == None:
        continue
    else:
        comp_norm = [i / j for i, j in zip(ast.literal_eval(element[1]), norm_basis)]
        occurrences_dict[element[0]] = comp_norm

total_ind_acad_sum = 0
dict_all = {}
for key, value in occurrences_dict.items():
    if sum(value) > 0:
        dict_all[key] = sum(value)/16
        total_ind_acad_sum = total_ind_acad_sum + sum(value)/16
    else:
        continue

europe_sum = 0
continents_count = {}
# Taking into account all european, asian and others countries:
for key, value in dict_all.items():
    if key in european_countries:
        print(key, value)
        europe_sum = europe_sum + value
# print('total from Europe:', europe_sum)

industry_sum = 0
other_world_sum = 0
for key, value in dict_all.items():
    if key not in european_countries and key in all_countries:
        print(key, value)
        other_world_sum = other_world_sum + value
    elif key not in all_countries:
        industry_sum = industry_sum + value

print('total from Europe:', europe_sum)
print('countries except Europe:', other_world_sum)
print('academia:', europe_sum+other_world_sum)
print('industry:', industry_sum)
print('all together:', total_ind_acad_sum, europe_sum+other_world_sum+industry_sum)


fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
recipe = ["European academy", "Academy not in Europe", "Industry"]
data = [europe_sum, other_world_sum, industry_sum]
# data = [float(x.split()[0]) for x in recipe]
# ingredients = [x.split()[-1] for x in recipe]
ingredients = ["European academy", "Not Europe", "Industry"]
def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)

wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          # title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

# ax.set_title("EAGE Annual C from 2006 to 2019")
plt.tight_layout()
plt.savefig('pie_plot.png', dpi=300)
plt.show()


quit()


total_sum = 0
list_sum = []
list_names = []
sorted_dict_all= {}
sorted_dict_all= sorted(dict_all.items(), key=lambda x:x[1])
percent_list = []
for item in sorted_dict_all:
    total_sum = total_sum + item[1]
    list_names.append(item[0])
    list_sum.append(item[1])

for item in sorted_dict_all:
    percent_list.append(round(item[1]/total_sum * 100, 2))



print(percent_list)
print(sum(percent_list))

list_names = [w.replace('Shell International Exploration and Production Inc.', 'Shell') for w in list_names]
list_names = [w.replace('Chevron Energy Technology Company', 'Chevron') for w in list_names]
list_names = [w.replace('United Kingdom of Great Britain and Nothern Ireland', 'United Kingdom') for w in list_names]
# print((sum(list_sum[1614:]))/sum(list_sum))
# print(len(list_sum[1614:]))
# quit()
list_to_print = list_sum[1614:]
# list_to_print.append(sum(list_sum[:1614]))
legend_to_print = list_names[1614:]
percent_list = percent_list[1614:]
legend_to_print_percent = []
print(sum(percent_list))
quit()
# legend_to_print.append('Companies that published\n less than 2 papers per year')
counter = 0
for items in legend_to_print:
    string = str(items+'\n'+str(percent_list[counter])+'%')
    legend_to_print_percent.append(string)
    counter +=1
    # print(counter)

# print(total_sum)
# print(len(sorted_sum_dict))
colors = cm.rainbow(np.linspace(0.15, 1, 11))
# colors = random.shuffle(colors)
# Change color
squarify.plot(sizes = list_to_print, label=legend_to_print_percent, color= colors, alpha=.6)
fig = plt.gcf()
fig.set_size_inches(13.8, 5.5)
# plt.figsize(8, 6)
# plt.figsize=(30, 20)
# plt.figsize(16, 10)

plt.tight_layout()
plt.axis('off')
plt.savefig('all_treemap.png', dpi=300)
plt.show()



quit()

sum_dict = {}


for key, value in occurrences_dict.items():
    if sum(value) > 0:
        if key in ind_dict.keys():
            sum_dict[key] = sum(value)/16
        else:
            continue
    else:
        continue

sorted_sum_dict = {}
sorted_sum_dict = sorted(sum_dict.items(), key=lambda x:x[1])
total_sum = 0
list_sum = []
list_names = []
for item in sorted_sum_dict:
    total_sum = total_sum + item[1]
    list_names.append(item[0])
    list_sum.append(item[1])
    # print(item)

list_names = [w.replace('Shell International Exploration and Production Inc.', 'Shell') for w in list_names]
list_names = [w.replace('Chevron Energy Technology Company', 'Chevron') for w in list_names]
list_names = [w.replace('LandOcean Energy Service Co', 'LandOcean') for w in list_names]
list_names = [w.replace('Rock Solid Images', 'RSI') for w in list_names]
list_names = [w.replace('Kuwait Oil Company', 'KOC') for w in list_names]
list_names = [w.replace('Petrochina', 'PetroChina') for w in list_names]
list_names = [w.replace('ION Geophysical', 'ION\nGeophysical') for w in list_names]

# count = 0
# for itm in list_sum:
#     if itm > 0:
#         count = count + 1
#     else:
#         continue
# print(count)

# We are printing 30 biggest companies
# print(list_names[1537:])
# print((sum(list_sum[:1537]))/sum(list_sum) )
# print(sum(list_sum[1537:]), sum(list_sum[:1537]), sum(list_sum) )
# quit()
# print(list_sum[1537:])
list_to_print = list_sum[1537:]
list_to_print.append(sum(list_sum[:1537]))
legend_to_print = list_names[1537:]
legend_to_print.append('Companies that published\n less than 2 papers per year')

# print(total_sum)
# print(len(sorted_sum_dict))
colors = cm.rainbow(np.linspace(0.15, 1, 11))
# colors = random.shuffle(colors)
# Change color
squarify.plot(sizes = list_to_print, label=legend_to_print, color= colors, alpha=.6)
fig = plt.gcf()
fig.set_size_inches(13.8, 5.5)
# plt.figsize(8, 6)
# plt.figsize=(30, 20)
# plt.figsize(16, 10)

plt.tight_layout()
plt.axis('off')
plt.savefig('treemap.png', dpi=300)
plt.show()
