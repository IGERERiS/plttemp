# coding=utf8
# Aim of this program is to retrieve data from the database
# and to print the graphs for the SEG MDPI paper
# Data available for the period: 1982-2019
# By default we plot graphs for the 1990-2019
# Timofey Eltsov
# January 5, 2020
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
from PIL import Image
# numb_pages - Number of pages for the corresponding year 1982-2019, 38 years in total
numb_pages = [520,	646,	856,	643,	715,	923,	1359,	1375,	1779,	1646,	1410,	1396,	1679,	1566,	2106,	2067,	2092,	2061,	2484,	2135,	2478,	2452,	2586,	2668,	3541,	3124,	3713,	4338,	4453,	4424,	4609,	5258,	5183,	5634,	5654,	6093,	5520, 5407]
numb_symbols_SEG = [3876563, 4300006, 5583145, 4577432, 4441406, 3181421, 4917848, 5030196, 6127287, 5740092, 5058741, 4768892, 6214099, 5583137, 6871658, 6897945, 7437265, 6917126, 8870421, 7731253, 9153100, 9268921, 9589137, 11012435, 11672829, 10477110, 11908644, 14437507, 14950656, 14756723, 15764247, 18001005, 17897258, 19463649, 20051753, 21314341, 19912746, 20069435]
aver_coauth_numb_SEG = [2.1589403973509933, 2.1052631578947367, 1.9828009828009827, 2.2161383285302594, 2.058219178082192, 2.148014440433213, 2.1649484536082473, 2.313131313131313, 2.3133462282398454, 2.2195121951219514, 2.2872062663185377, 2.355, 2.504291845493562, 2.6057906458797326, 2.6205128205128205, 2.669741697416974, 2.734061930783242, 2.837638376383764, 2.908805031446541, 2.8248175182481754, 2.9011164274322168, 3.103448275862069, 3.0693815987933637, 3.127565982404692, 3.1204481792717087, 3.126782884310618, 3.3454790823211877, 3.2354948805460753, 3.308132875143184, 3.44815668202765, 3.552836484983315, 3.433628318584071, 3.494959677419355, 3.571296296296296, 3.476449275362319, 3.6575342465753424, 3.6621743036837375, 3.9009259259259259259259259259259]
aver_pages_SEG = [i / 3000 for i in numb_symbols_SEG]
# numb_symbols_EAGE - Number of symbols for each of the corresponding year 2001-2019, 19 years in total
numb_symbols_EAGE = [5504576, 6691125, 5001435, 6697122, 9786123, 5271969, 6992646, 7889951, 8179235, 11006371, 10703326, 15831187, 16963000, 13753199, 13615665, 13641114, 15426915, 14449214, 12885065]
aver_pages_EAGE = [ i / 3000 for i in numb_symbols_EAGE]
# numb_papers - Number of articles for the corresponding year 1982-2019, 38 years in total
numb_articles = [302,	323,	407,	347,	292,	277,	388,	396,	517,	451,	383,	400,	466,	449,	585,	542,	549,	542,	636,	548,	627,	638,	663,	682,	714,	631,	741,	879,	873,	868,	899,	1017,	992,	1080,	1104,	1168,	1113, 1080]
oil_price = [32.38,	29.04,	28.2,	27.01,	13.53,	17.73,	14.24,	17.31,	22.26,	18.62,	18.44,	16.33,	15.53,	16.86,	20.29,	18.86,	12.28,	17.44,	27.6,	23.12,	24.36,	28.1,	36.05,	50.59,	61,	69.04,	94.1,	60.86,	77.38,	107.46,	109.45,	105.87,	96.29,	49.49,	40.76,	52.51,	69.78, 63.83]
end_year = 2019
norm_basis = aver_pages_SEG

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
# Summ of all the elements in one list to find groups of words impact
def sum_of_lists(input):
    output = zerolistmaker(norm_basis)
    for item in input:
        output = [x + y  for x, y in zip(output, item)]
    return output


def co_aouth_figs():
    print(aver_coauth_numb_SEG)


def build_word_figs():
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    database_name = 'SEGgrams.sqlite'
    start_year = 1982
    left_border = 1990
    data_to_print = []
    legend_to_print = []
    summ_total = 0
    counter = 0
    data ={ "most_popl_rocks" : ['shale', 'sandstone', 'limestone',  'basalt', 'gneiss'],
            "some_rocks" : ['shale', 'carbonate', 'sandstone', 'limestone', 'volcanic' ],
            "shale_types" : ['Barnett', 'Eagle', 'Marcellus', 'Haynesville'],
            "hudr_frac" : ['hydraulic fracturing', 'frac', 'fracking', 'shale gas', 'gas shale', 'toc', 'unconventional'],
            "conv_nn_deep" : ['convolutional neural', 'deep learning', 'artificial intelligence', 'neural network', 'field data' ],
            "nn_related" : ['convolutional neural', 'training data', 'machine learning', 'deep learning', 'training set', 'learning method', 'neural network' ],
            "most_grow_si" : ['learning', 'Marchenko', 'trained', 'generative', 'fibre', 'fiber'] ,
            "most_decl_si" : ['basalt', 'GPU', 'Barnett'],
            "most_grow_bi" : ['machine learning', 'training data', 'igneous rock', 'convolutional neural', 'computer vision', 'tight sandstone'],
            "most_decl_bi" : ['beam migration', 'source array', 'receiver depth', 'depth level', 'Barnett shale', 'receiver ghost'],
            "most_grow_tri" : ['convolutional neural network', 'seismic facies classification', 'distributed acoustic sensing', 'ground penetrating radar'],
            "most_decl_tri" : ['waveequation migration velocity', 'multiple attenuation algorithm', 'Eagle Ford Shale', 'Gassmann fluid substitution', 'towed streamer em'],
            "fwi_rtm_psdm2" : ['prestack depth migration', 'full waveform inversion', 'reverse time migration'],
            "fwi_rtm_psdm" : ['PSDM', 'FWI', 'RTM'],
            "stu_faculty" : ['student', 'faculty', 'researcher', 'engineer', 'scientist'],
            "sigrams_int2" : ['monitoring', 'efficiency', 'future', 'legacy'],
            "time_perm_jur_cret" : ['Permian', 'Jurassic', 'Cretaceous'], }

    for key, value in data.items():
        lists = value
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[key]

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

        # Exclusions:
        if key == "hudr_frac":
            ts0 = all_words_norm[0]
            ts1 = all_words_norm[1]
            ts2 = all_words_norm[2]
            ts3 = all_words_norm[3]
            ts4 = all_words_norm[4]
            ts5 = all_words_norm[5]
            ts6 = all_words_norm[6]
            ts012 = []
            ts34 = []
            ts012 = [x + y + c for x, y, c in zip(ts0, ts1, ts2)]
            ts34 = [x + y  for x, y in zip(ts3, ts4)]
            ts = [ts012, ts34, ts5, ts6]
            all_words_norm = ts
            legend_to_print = ['fracking', 'shale gas', 'toc', 'unconventional']
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

        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
        ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

        # Here we set the parameters of the figure
        plt.xlabel('Year', fontsize=fontsize_det)
        plt.ylabel(y_ax_label, fontsize=fontsize_det)
        plt.grid(True)
        plt.tight_layout()
        # The legend position
        if key == "fwi_rtm_psdm2":
            plt.legend(legend_to_print, loc = "upper right", fontsize=fontsize_det)
        else:
            plt.legend(legend_to_print, loc = "upper left", fontsize=fontsize_det)
        # The range of the axes
        plt.axis([left_border, 2019, minimum, maximum], fontsize=fontsize_det)
        if len(lists[0]) > 3 and len(lists[1]) > 3:
            name = str(lists[0][:4] +'_' + lists[1][:4])
        else:
            name = str(lists[0][:3] +'_' + lists[1][:3])
        # print(name)
        plt.savefig('K:\\python\\SQL\\images\\'+key+'.png', dpi=300)
        # plt.show()
        plt.close()
        counter += 1

    # img = Image.new('RGB', (3620, 1440))
    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\most_grow_si.png')
    img2 = Image.open('K:\\python\\SQL\\images\\most_decl_si.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1790,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\si_grow_decl.png")
    img.close()

    # img = Image.new('RGB', (3620, 1440))
    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\most_grow_bi.png')
    img2 = Image.open('K:\\python\\SQL\\images\\most_decl_bi.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1790,0))
    img.paste(img2, (1910,0))  
    img.save("K:\\python\\SQL\\images\\bi_grow_decl.png")
    img.close()
        
    # img = Image.new('RGB', (3620, 1440))
    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\most_grow_tri.png')
    img2 = Image.open('K:\\python\\SQL\\images\\most_decl_tri.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1790,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\tri_grow_decl.png")
    img.close()

    # img = Image.new('RGB', (3700, 1440))
    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\shale_types.png')
    img2 = Image.open('K:\\python\\SQL\\images\\hudr_frac.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1850,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\shale_frac.png")
    img.show()
    img.close()

    # img = Image.new('RGB', (3700, 1440))
    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\fwi_rtm_psdm2.png')
    img2 = Image.open('K:\\python\\SQL\\images\\fwi_rtm_psdm.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1850,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\fwi_rtm_psdm_both.png")
    img.show()
    img.close()


    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\stu_faculty.png')
    img2 = Image.open('K:\\python\\SQL\\images\\sigrams_int2.png')
    img.paste(img1, (0,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\sigrams_int.png")
    img.show()
    img.close()

    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\conv_nn_deep.png')
    img2 = Image.open('K:\\python\\SQL\\images\\nn_related.png')
    img.paste(img1, (0,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\nn_related_all.png")
    img.close()

   
def build_org_figs():
    fontsize_det = 13
    start_year = 1982
    end_year = 2019
# Academy dictionaty
    conn = sqlite3.connect('Academy_by_Country.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Academy")
    data_aca=cursor.fetchall()
    academy_dict = {}
    for element in data_aca:
        academy_dict[element[0]] = eval(element[1])
# Industry dictionaty
    conn = sqlite3.connect('Industry.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Industry")
    data_ind=cursor.fetchall()
    industry_dict = {}
    for element in data_ind:
        industry_dict[element[0]] = eval(element[1])
# Data for printing
    conn = sqlite3.connect('SEG_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SEG_affiliations_data")
    data_aff=cursor.fetchall()
    aff_dict = {}
    for element in data_aff:
        aff_dict[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SEG)]

    list_ind = []
    list_aca = []
    for key, value in aff_dict.items():
        if key in industry_dict.keys():
            list_ind.append(value)
        if key in academy_dict.keys():
            list_aca.append(value)

    print_ind = sum_of_lists(list_ind)
    print_aca = sum_of_lists(list_aca)
    print_aca_no_ch = [i - j for i, j in zip(print_aca, aff_dict["China"])]
    s = list(range(start_year, end_year+1, 1))
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    lns1 = plt.plot(s, print_aca, 'r*-',linewidth=1.2 , markersize = 1.5, label="Academy")
    lns2 = plt.plot(s, print_ind,'c>-',  linewidth=1.2 , markersize = 1.5, label="Industry")
    lns3 = plt.plot(s, print_aca_no_ch, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academy without China")
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    # plt.legend()
    plt.axis([1982, 2019, 0, 650], labelsize = fontsize_det)
    ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    lns = lns1+lns2+lns3+lns4
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 120], labelsize = fontsize_det)
    plt.savefig('C:\\temp\\Tex\\MDPI_SEG\\images\\acad_indus_plot.png', dpi=300)
    plt.close()

    plt.rcdefaults()

    lns1 = plt.plot(s, aff_dict["Schlumberger"], 'b*-',linewidth=0.6 , markersize = 1.5,  label="Schlumberger")
    lns2 = plt.plot(s, aff_dict["WesternGeco"], 'r^-',linewidth=.6 , markersize = 1.5, label="WesternGeco")
    lns3 = plt.plot(s, aff_dict["CGG"], 'mx--', linewidth=.6 , markersize = 1.5, label="CGG")
    lns4 = plt.plot(s, aff_dict["BGP"], 'p--',linewidth=.6 , markersize = 1.5, label="BGP")
    
    plt.grid(True)

    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)


    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 65], labelsize = fontsize_det)
    ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.axis([1982, 2019, 0, 120])
    ax2.tick_params(axis='y', labelsize=fontsize_det)
    color = 'tab:green'
    ax2.set_ylabel('Price, $', color=color, size = 13)  # we already handled the x-label with ax1
    lns5 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    lns = lns1+lns2+lns3+lns4+lns5
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0, fontsize=fontsize_det)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.tight_layout() 

    plt.savefig('K:\\python\\SQL\\images\\oil_service.png', dpi=300)
    plt.close()
    
    plt.rcdefaults()

    plt.plot(s, aff_dict["Petrochina"], 'c*-',linewidth=0.7 , markersize = 1.5,  label="PetroChina")
    plt.plot(s, aff_dict["Shell International Exploration and Production Inc."], 'g-o',linewidth=0.5 , markersize = 1.5, label="Shell")
    plt.plot(s, aff_dict["Saudi Aramco"], 'b--', linewidth=0.9 , markersize = 1.5, label="Saudi Aramco")
    plt.plot(s, aff_dict["ExxonMobil"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="ExxonMobil")
    plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
   
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 35], labelsize = fontsize_det)
    plt.legend(loc = "upper left", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\oil_companies.png', dpi=300)
    plt.close()

    # img = Image.new('RGB', (3740, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\oil_service.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\oil_companies.png')
    # img.paste(img1, (-40,0))
    # img.paste(img2, (1830,0))
    # img.save("K:\\python\\SQL\\images\\oil_and_service.png")
    # img.show()
    # img.close()

    plt.rcdefaults()

    plt.plot(s, aff_dict["United States of America"], 'b*-',linewidth=0.7 , markersize = 1.5,  label="USA")
    plt.plot(s, aff_dict["China"], 'g-o',linewidth=1 , markersize = 1.5, label="China")
    plt.plot(s, aff_dict["Canada"], 'm--', linewidth=0.9 , markersize = 1.5, label="Canada")
    plt.plot(s, aff_dict["Netherlands"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="Netherlands")
    # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
   
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 230], labelsize = fontsize_det)
    plt.legend(loc = "upper left", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\4_first_countries.png', dpi=300)
    # plt.show()
    plt.close()

    plt.rcdefaults()

    plt.plot(s, aff_dict["France"], 'k*-',linewidth=1 , markersize = 1.5,  label="France")
    plt.plot(s, aff_dict["United Kingdom of Great Britain and Nothern Ireland"], 'c-.', linewidth=1.1 , markersize = 1.5, label="United Kingdom")
    plt.plot(s, aff_dict["Germany"], 'y-o',linewidth=1.7 , markersize = 1.5, label="Germany")
    plt.plot(s, aff_dict["Australia"], 'r--',linewidth=1.2 , markersize = 1.5,  label="Australia")
    # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
   
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 37], labelsize = fontsize_det)
    plt.legend(loc = "upper right", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\4_second_countries.png', dpi=300)
    plt.close()


    img = Image.new('RGB', (3740, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\4_first_countries.png')
    img2 = Image.open('K:\\python\\SQL\\images\\4_second_countries.png')
    img.paste(img1, (-40,0))
    img.paste(img2, (1850,0))
    img.save("K:\\python\\SQL\\images\\8_countries.png")
    img.show()
    img.close()
    
    # for key, value in aff_dict.items():
    #     if key in academy_dict.keys():
    #         print(sum(value), key)



def plot_hystogram():
    y_ax_label = 'No. of words/page'
    fontsize_det = 13
    conn = sqlite3.connect('SEGgrams.sqlite')
    cursor = conn.cursor()
    
    threewords = ['lateral velocity variation', 'seismic data processing', 'well log data', 'transversely isotropic medium', 'surface seismic data', 'seismic reflection data', 'shear wave velocity', 'migration velocity analysis', 'reverse time migration', 'full waveform inversion']
    twowords = ['wave propagation', 'velocity analysis', 'source receiver', 'field data', 'shear wave', 'depth migration', 'wave equation', 'data set', 'velocity model', 'seismic data']
    onewords = ['field',	'well', 'source',	'time',	'method',	'wave',	'model',	'velocity',	'seismic',	'data']

    w3_to_print = {}
    w3_leg_to_print = []
    w2_to_print = {}
    w2_leg_to_print = []
    w1_to_print = {}
    w1_leg_to_print = []
    # numb_pages
    for item in threewords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w3_to_print[records[0]] = sum(my_list)/len(aver_pages_SEG)
    my_list = []
    for item in twowords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w2_to_print[records[0]] = sum(my_list)/len(aver_pages_SEG)
    for item in onewords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w1_to_print[records[0]] = sum(my_list)/len(aver_pages_SEG)

    # w3_to_print.reverse();    w2_to_print.reverse();    w1_to_print.reverse()
    # threewords.reverse();    twowords.reverse();    onewords.reverse()
    listofTuples3 = sorted(w3_to_print.items() ,  key=lambda x: x[1])
    listofTuples2 = sorted(w2_to_print.items() ,  key=lambda x: x[1])
    listofTuples1 = sorted(w1_to_print.items() ,  key=lambda x: x[1])
    w3_to_print = {}
    w2_to_print = {}
    w1_to_print = {}
    for item in listofTuples3: w3_to_print[item[0]] = float(item[1])
    for item in listofTuples2: w2_to_print[item[0]] = float(item[1])
    for item in listofTuples1: w1_to_print[item[0]] = float(item[1])

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(4.8,5))
    y_pos = np.arange(len(w3_to_print.keys()))
    ax.barh(y_pos, list(w3_to_print.values()), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w3_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\trigrams.png', dpi=300)
    plt.close()

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(3.5, 5))
    y_pos = np.arange(len(w2_to_print.keys()))
    ax.barh(y_pos, w2_to_print.values(), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w2_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\bigrams.png', dpi=300)
    plt.close()

    plt.show()
    fig, ax = plt.subplots(figsize= (2.7, 5))
    y_pos = np.arange(len(w1_to_print.keys()))
    ax.barh(y_pos, w1_to_print.values(), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w1_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\sigrams.png', dpi=300)
    plt.close()

    img = Image.new('RGB', (3150, 1460))
    img1 = Image.open('K:\\python\\SQL\\images\\trigrams.png')
    img2 = Image.open('K:\\python\\SQL\\images\\bigrams.png')
    img3 = Image.open('K:\\python\\SQL\\images\\sigrams.png')
    
    img.paste(img3, (0,0))
    img.paste(img2, (730,0))
    img.paste(img1, (1750,0))

    img.save("K:\\python\\SQL\\images\\grams_hyst.png")
    img.show()
    img.close()


def groups_printing():
    database_name = 'SEGgrams.sqlite'
    norm_basis = aver_pages_SEG
    start_year = 1982
    left_border = 1990
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    # We read the input data from the terminal
    # items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
    data_to_print = []
    legend_to_print = []
    total_printing_data = []
    summ_total = 0
    counter = 0
    data = [['sedimentary', 'clastic', 'breccia', 'conglomerate', 'sandstone', 'siltstone', 'shale', 'chert', 'flint', 'dolomite', 'limestone', 'carbonate', 'coal'],
    ['igneous', 'intrusive', 'diorite', 'gabbro', 'granite', 'pegmatite', 'peridotite', 'extrusive', 'andesite', 'basalt', 'dacite', 'obsidian', 'pumice', 'rhyolite', 'scoria', 'tuff', 'volcanics'],
    ['metamorphic', 'gneiss', 'phyllite', 'schist', 'slate', 'hornfels', 'marble', 'quartzite', 'novaculite', 'soapstone']
    ]
    # We consider the case when we have only one word/phrase to print
    # We consider the case when we have a number of word(s)/phrase(s) to print
    # plt.figure(figsize=(9,5))
    for lists in data:
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                end = time.time()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[counter]
    
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
    
        total_printing_data.append(all_words_norm)
    
    groups_to_print = []
    for element in total_printing_data:
        groups_to_print.append(sum_of_lists(element))
    
    # print(groups_to_print)
    legend_to_print = ['sedimentary', 'igneous', 'metamorphic']
    # Here we are plotting the requestqed word(s)/phrase(s):
    colors = cm.rainbow(np.linspace(0.15, 1, len(groups_to_print)))
    ts = groups_to_print
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
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel(y_ax_label, fontsize=fontsize_det)
    plt.grid(True)
    plt.tight_layout()
    # The legend position
    plt.legend(legend_to_print, loc = "lower left", fontsize=fontsize_det)
    # The range of the axes
    # plt.axis([left_border, 2019, minimum, maximum])
    plt.axis([left_border, 2019, 0.002, 1])
    # if len(lists[0]) > 3 and len(lists[1]) > 3:
    #     name = str(lists[0][:4] +'_' + lists[1][:4])
    # else:
    #     name = str(lists[0][:3] +'_' + lists[1][:3])
    # # print(name)
    plt.grid(b=True, which='minor', color='grey', linestyle='--', linewidth=0.35)
    plt.yscale('log')
    plt.savefig('K:\\python\\SQL\\images\\rock_types.png', dpi=300)
    # plt.show()
    plt.close()


    img = Image.new('RGB', (3700, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\rock_types.png')
    img2 = Image.open('K:\\python\\SQL\\images\\most_popl_rocks.png')
    img.paste(img1, (0,0))
    img.paste(img2, (1850,0))
    img.save("K:\\python\\SQL\\images\\rocks.png")
    img.show()
    img.close()

# bbb = plot_hystogram()
# bbb = build_org_figs()
bbb = build_word_figs()
# bbb = groups_printing()