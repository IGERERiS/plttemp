# coding=utf8
# Aim of this program is find words/phrases with better correlation
# Timofey Eltsov
# January 5, 2020
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import numpy
import sqlite3
import time
import ssl
import math
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
# database_ind = input('Please indicate the database you want to check. There are two options: SEG and EAGE\n')
# if database_ind == 'SEG' or database_ind == 'EAGE':
# # Here we set the database name:
#     if database_ind == 'EAGE':
database_name = 'SEGgrams.sqlite'
norm_basis = aver_pages_SEG
start_year = 1982
left_border = 1990

conn = sqlite3.connect(database_name)
cursor = conn.cursor()
cursor.execute("SELECT * FROM WordsData")
data_an=cursor.fetchall()

comp_norm = []
dictionary = {}
dictionary_flt = {}
for element in data_an:
    comp_norm = [i / j for i, j in zip(ast.literal_eval(element[1]), norm_basis)]
    dictionary[element[0]] = comp_norm
    if sum(comp_norm) > 0.02:
        count_null = 0
        for item in comp_norm:
            if item == 0:
                count_null += 1
            else:
                continue

        if count_null > 25:
            continue
        else:
            dictionary_flt[element[0]] = comp_norm

search_list = dictionary_flt['toc'][8:]
# print(search_list)
search_list.reverse()


for key, value in dictionary_flt.items():
    if numpy.corrcoef(value[8:], dictionary_flt['water'][8:])[0, 1] > 0.75:
        print(key)
quit()
# for key, value in dictionary_flt.items():
#     if numpy.corrcoef(value[8:], search_list)[0, 1] > 0.8:
#         print(key)
rang = []
for i in range(-300, 300): rang.append(i/10+1/10)
# print(rang)
print(len(rang))
l_border = round(len(rang)/2)
r_border = l_border+30
f_x = []
for x in rang: f_x.append(1/2*math.pi*math.exp(-math.pow(x, 2)/2))
# print(f_x)

plt.plot(rang[l_border:r_border], f_x[l_border:r_border], 'b-', linewidth=1)
plt.show()

for key, value in dictionary_flt.items():
    if numpy.corrcoef(value[8:], f_x[l_border:r_border])[0, 1] > 0.85:
        print(key)

# dictionary_flt['parallel computer']

quit()
# print(type(element))
# print(dictionary)
# quit()
# # print(dictionary_flt)
# file_out_1=open('K:\\python\\SQL\\output1.txt', 'w')
# file_out_2=open('K:\\python\\SQL\\output2.txt', 'w')
# for key, value in dictionary_flt.items():
#     for key2, value2 in dictionary_flt.items():
#         if numpy.corrcoef(value[8:], value2[8:])[0, 1] > 0.96 and key is not key2:
#             print(key, '<=>', key2, file = file_out_1)
#         if numpy.corrcoef(value[8:], value2[8:])[0, 1] < -0.96 and key is not key2:
#             print(key, '<=>', key2, file = file_out_2)
#
# print(len(dictionary), len(dictionary_flt))

# print(data_an)
quit()

# all_words_norm = []
# # We check if data is not zero
# for vals in data_to_print:
#     if isinstance(vals, list):
# # We normalize each number of occurrences by number of pages at corresponding year
#         words_norm = [i / j for i, j in zip(vals, norm_basis)]
#         all_words_norm.append(words_norm)
#         for part in vals:
#             summ_total = summ_total + part
#     else:
#         summ_total = summ_total + vals
# # We normalize each number of occurrences by number of pages at corresponding year
#         words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
#         all_words_norm = words_norm
# if summ_total < 0.00001:
#     print('\nNone of the requsted words are present in the database.')
#     print('Please, try again')
#     quit()
#
# # Here we are plotting the requestqed word(s)/phrase(s):
# colors = cm.rainbow(np.linspace(0.15, 1, len(all_words_norm)))
# ts = all_words_norm
# s = list(range(start_year, end_year+1, 1))
# # We set the appropriate scale for all the elements in the list
# for vals in ts:
# # The multiple entries case
#     if isinstance(vals, list):
#         maximum = [max(ts[ii]) for ii in range(0, len(ts))]
#         minimum = [min(ts[ii]) for ii in range(0, len(ts))]
#         maximum = max(maximum)
#         minimum = min(minimum)
#         maximum = maximum + 0.1*maximum
#         minimum = minimum - 0.1*minimum
#         for y, c in zip(ts, colors):
#             plt.plot(s, y, linewidth=1.1, color=c)
# # The single enrtry case
#     else:
#         maximum = max(ts)
#         minimum = min(ts)
#         maximum = maximum + 0.1*maximum
#         minimum = minimum - 0.1*minimum
#         plt.plot(s, ts, 'b-', linewidth=1)
#
# if minimum < 0:
#     minimum = 0
#
# # Here we set the parameters of the figure
# plt.xlabel('Year')
# plt.ylabel('Occurrence/pages')
# plt.grid(True)
# # The legend position
# plt.legend(legend_to_print, loc = "upper left")
# # The range of the axes
# plt.axis([left_border, 2019, minimum, maximum])
# plt.savefig('figure.png', dpi=300)
# end = time.time()
# print('The calculation time:', round(end-start, 3))
# plt.show()
