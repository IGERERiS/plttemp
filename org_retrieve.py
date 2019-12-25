# coding=utf8
# Aim of this program is to retrieve data from the databases - SEG or EAGE
# and to print the graph with requested industrial or academic companies
# Data available for the period: 1982-2019
# By default we plot graphs for the 1982-2019
# Timofey Eltsov
# December 16, 2019
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import sqlite3
import time
import ssl
import ast
# aver_coauth_numb_SEG - Average number of authors per paper (SEG Annual meetings). 1982-2019, 38 years in total
aver_coauth_numb_SEG = [2.1589403973509933, 2.1052631578947367, 1.9828009828009827, 2.2161383285302594, 2.058219178082192, 2.148014440433213, 2.1649484536082473, 2.313131313131313, 2.3133462282398454, 2.2195121951219514, 2.2872062663185377, 2.355, 2.504291845493562, 2.6057906458797326, 2.6205128205128205, 2.669741697416974, 2.734061930783242, 2.837638376383764, 2.908805031446541, 2.8248175182481754, 2.9011164274322168, 3.103448275862069, 3.0693815987933637, 3.127565982404692, 3.1204481792717087, 3.126782884310618, 3.3454790823211877, 3.2354948805460753, 3.308132875143184, 3.44815668202765, 3.552836484983315, 3.433628318584071, 3.494959677419355, 3.571296296296296, 3.476449275362319, 3.6575342465753424, 3.6621743036837375, 3.9009259259259259259259259259259]
# aver_coauth_numb_EAGE - Average number of authors per paper (EAGE Annual meetings). 2001-2019, 19 years in total
aver_coauth_numb_EAGE = [3.05, 3.0676258992805754, 2.979466119096509, 3.1364341085271317, 3.152269399707174, 3.044776119402985, 3.117283950617284, 3.2708978328173375, 3.2417127071823204, 3.3980044345898004, 3.1833872707659117, 3.227355072463768, 3.4643714971977584, 3.646404109589041, 3.7708333333333335, 3.671511627906977, 3.599670510708402, 3.6703577512776833, 3.9076923076923076]
# The reference data from Earht and planetary science
ref_data = [2.285361,2.269854,2.285205,2.274893, 2.32184, 2.352931, 2.433209, 2.402235, 2.433422, 2.49702, 2.594231, 2.581554, 2.727233, 2.789873, 2.874077, 2.885946, 3.018021, 3.166208, 3.372227, 3.288681, 3.346355, 3.463061, 3.437281, 3.519684, 3.67232, 3.747994, 3.896395, 3.848252, 4.055962, 4.122729, 4.207524, 4.246959, 4.315808, 4.348695, 4.480921, 4.601956, 4.730707]
end_year = 2019
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
# Which database do you want to check
database_ind = input('Please indicate the database you want to check. There are two options: SEG and EAGE\n')
if database_ind == 'SEG' or database_ind == 'EAGE':
# Here we set the database name:
    if database_ind == 'EAGE':
        database_name = 'EAGE_affiliations_data.sqlite'
        norm_basis = aver_coauth_numb_EAGE[5:]
        start_year = 2006
        left_border = 2006
    if database_ind == 'SEG':
        database_name = 'SEG_affiliations_data.sqlite'
        norm_basis = aver_coauth_numb_SEG
        start_year = 1982
        left_border = 1990
    pass
else:
    print('Wrong database indicator. Please try use \'SEG\' or \'EAGE\'\n.\n'); quit()
# We read the input data from the terminal
items = input('Please quote the company or and country of academia you want to check.\nExample1: \'BP\'\nIf more than one please use the list format:\nExample2:  [\'Saudi Aramco\', \'Chevron Energy Technology Company\', \'Petrochina\', \'China\']\nPlease type company or country you want to check here:\n')
start = time.time()
if len(items) == 0: print('Error. Input is an empty string. Please try again.\n'); quit()
if items == None: print('Wrong input format. Please try again.\n'); quit()
data = ast.literal_eval(items)
data_to_print = []
legend_to_print = []
summ_total = 0
# We consider the case when we have only one word/phrase to print
if isinstance(data, str):
    print('One word/phrase')
    item = data
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
# We check if the entry exists in the database
# If one of the entries does not exist in the database, we will assign a zero value to it
# We will print the graph only if one of the entries exists in the database
    print(database_name)
    cursor.execute("SELECT Title FROM "+database_name.replace('.sqlite', '')+" WHERE Title = ?", (data,) )
    data_in=cursor.fetchall()
    if len(data_in)==0:
        print('There is no entry named \'%s\''%data)
        print('Please, try again')
        quit()
    else:
        cursor = conn.execute("SELECT * FROM "+database_name.replace('.sqlite', '')+" WHERE Title= ?", (item,))
        records = cursor.fetchone()
        end = time.time()
        conn.close()
        legend_to_print.append(records[0])
        data_temp = ast.literal_eval(records[1])
        data_to_print = make_float(data_temp)

# We consider the case when we have a number of word(s)/phrase(s) to print
elif isinstance(data, list):
    print('\nThe number of entries is', len(data))
    for item in data:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT Title FROM "+database_name.replace('.sqlite', '')+" WHERE Title = ?", (item,))
        data_in=cursor.fetchall()
        if len(data_in)==0:
            print('\nThere is no entry named \'%s\''%item)
            data_to_print.append(zerolistmaker(norm_basis))
            legend_to_print.append(item)
        else:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor = conn.execute("SELECT * FROM "+database_name.replace('.sqlite', '')+" WHERE Title= ?", (item,))
            records = cursor.fetchone()
            end = time.time()
            conn.close()
            my_list = ast.literal_eval(records[1])
            data_to_print.append(make_float(my_list))
            legend_to_print.append(records[0])

all_words_norm = []
# We check if data is not zero
for vals in data_to_print:
    if isinstance(vals, list):
# We normalize each number of occurrences by number of pages at corresponding year
        words_norm = [i / j for i, j in zip(vals, norm_basis)]
        all_words_norm.append(words_norm)
        for part in vals:
            summ_total = summ_total + part
    else:
        summ_total = summ_total + vals
# We normalize each number of occurrences by number of pages at corresponding year
        words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
        all_words_norm = words_norm
if summ_total < 0.00001:
    print('\nNone of the requsted words are present in the database.')
    print('Please, try again')
    quit()

# Here we are plotting the requestqed word(s)/phrase(s):
colors = cm.rainbow(np.linspace(0.15, 1, len(all_words_norm)))
ts = all_words_norm
s = list(range(start_year, end_year+1, 1))
# We set the appropriate scale for all the elements in the list
for vals in ts:
# The multiple entries case
    if isinstance(vals, list):
        maximum = [max(ts[ii]) for ii in range(0, len(ts))]
        minimum = [min(ts[ii]) for ii in range(0, len(ts))]
        maximum = max(maximum)
        minimum = min(minimum)
        maximum = maximum + 0.1*maximum
        minimum = minimum - 0.1*minimum
        for y, c in zip(ts, colors):
            plt.plot(s, y, linewidth=1.1, color=c)
# The single enrtry case
    else:
        maximum = max(ts)
        minimum = min(ts)
        maximum = maximum + 0.1*maximum
        minimum = minimum - 0.1*minimum
        plt.plot(s, ts, 'b-', linewidth=1)

if minimum < 0:
    minimum = 0

# Here we set the parameters of the figure
plt.xlabel('Year')
plt.ylabel('Average number of publications')
plt.grid(True)
# The legend position
plt.legend(legend_to_print, loc = "upper left")
# The range of the axes
plt.axis([left_border, 2019, minimum, maximum])
plt.savefig('figure1.png', dpi=300)
end = time.time()
print('The calculation time:', round(end-start, 3))
plt.show()
