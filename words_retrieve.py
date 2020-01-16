# coding=utf8
# Aim of this program is to retrieve data from the database
# and to print the graph with requested words and phrases
# Data available for the period: 1982-2019
# By default we plot graphs for the 1990-2019
# Timofey Eltsov
# December 9, 2019
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
# numb_pages - Number of pages for the corresponding year 1982-2019, 38 years in total
numb_pages = [520,	646,	856,	643,	715,	923,	1359,	1375,	1779,	1646,	1410,	1396,	1679,	1566,	2106,	2067,	2092,	2061,	2484,	2135,	2478,	2452,	2586,	2668,	3541,	3124,	3713,	4338,	4453,	4424,	4609,	5258,	5183,	5634,	5654,	6093,	5520, 5407]
numb_symbols_SEG = [3876563, 4300006, 5583145, 4577432, 4441406, 3181421, 4917848, 5030196, 6127287, 5740092, 5058741, 4768892, 6214099, 5583137, 6871658, 6897945, 7437265, 6917126, 8870421, 7731253, 9153100, 9268921, 9589137, 11012435, 11672829, 10477110, 11908644, 14437507, 14950656, 14756723, 15764247, 18001005, 17897258, 19463649, 20051753, 21314341, 19912746, 20069435]
aver_pages_SEG = [i / 3000 for i in numb_symbols_SEG]
# numb_symbols_EAGE - Number of symbols for each of the corresponding year 2001-2019, 19 years in total
numb_symbols_EAGE = [5504576, 6691125, 5001435, 6697122, 9786123, 5271969, 6992646, 7889951, 8179235, 11006371, 10703326, 15831187, 16963000, 13753199, 13615665, 13641114, 15426915, 14449214, 12885065]
aver_pages_EAGE = [i / 3000 for i in numb_symbols_EAGE]
# numb_papers - Number of articles for the corresponding year 1982-2019, 38 years in total
numb_articles = [302,	323,	407,	347,	292,	277,	388,	396,	517,	451,	383,	400,	466,	449,	585,	542,	549,	542,	636,	548,	627,	638,	663,	682,	714,	631,	741,	879,	873,	868,	899,	1017,	992,	1080,	1104,	1168,	1113, 1080]
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
        database_name = 'EAGEgrams.sqlite'
        norm_basis = aver_pages_EAGE
        start_year = 2001
        left_border = 2001
    if database_ind == 'SEG':
        database_name = 'SEGgrams.sqlite'
        norm_basis = aver_pages_SEG
        start_year = 1982
        left_border = 1990
    pass
else:
    print('Wrong database indicator. Please try use \'SEG\' or \'EAGE\'\n.\n'); quit()
# We read the input data from the terminal
items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
start = time.time()
if len(items) == 0: print('Error. Input is an empty string. Please try again.\n'); quit()
if items == None: print('Wrong input format. Please try again.\n'); quit()
data = ast.literal_eval(items.lower())
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
    cursor.execute("SELECT words FROM WordsData WHERE words = ?", (data,))
    data_in=cursor.fetchall()
    if len(data_in)==0:
        print('There is no entry named \'%s\''%data)
        print('Please, try again')
        quit()
    else:
        cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item,))
        records = cursor.fetchone()
        end = time.time()
        conn.close()
        legend_to_print.append(records[0])
        data_temp = ast.literal_eval(records[1])
        data_to_print = make_float(data_temp)

# We consider the case when we have a number of word(s)/phrase(s) to print
elif isinstance(data, list):
    print('\nThe number of word(s)/phrase(s) is', len(data))
    for item in data:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item,))
        data_in=cursor.fetchall()
        if len(data_in)==0:
            print('\nThere is no entry named \'%s\''%item)
            data_to_print.append(zerolistmaker(norm_basis))
            legend_to_print.append(item)
        else:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item,))
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
maximum = []
minimum = []
for vals in ts:
# The multiple entries case
    if isinstance(vals, list):
        maximum.append(max(vals[8:]))
        minimum.append(min(vals[8:]))
        # maximum = max(maximum)
        # minimum = min(minimum)
        for y, c in zip(ts, colors):
            plt.plot(s, y, linewidth=1.1, color=c)
# The single enrtry case
    else:
        maximum = max(ts)
        minimum = min(ts)
        maximum = maximum + 0.1*maximum
        minimum = minimum - 0.1*minimum
        plt.plot(s, ts, 'b-', linewidth=1)

# if min(minimum) < 0:
minimum = 0

if isinstance(maximum, list):
    maximu = max(maximum)
else:
    maximu = maximum
    
maximu = maximu + 0.1*maximu

# for element in ts:
#     print(element)


# Here we set the parameters of the figure
plt.xlabel('Year')
plt.ylabel('No. of words/page')
plt.grid(True)
# The legend position
plt.legend(legend_to_print, loc = "upper left")
# The range of the axes
plt.axis([left_border, 2019, minimum, maximu])
plt.savefig('figure.png', dpi=300)
end = time.time()
print('The calculation time:', round(end-start, 3))
plt.show()
