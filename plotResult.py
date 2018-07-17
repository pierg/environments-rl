import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import glob
from random import randint
import configurations.config_grabber as cg
from pathlib import Path
import screenHelper
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 15})
"""
File used to create a graph from a csv file and the name of the columns that need to be used
"""


def plot_result(scale,tab,fileName,resultFileName):
    array = [[] for i in range(0,2)]
    array2 = [[] for i in range(0,2)]
    column_number = [0 for i in range(0,2)]
    list_of_name = ["" for i in range(0,2)]
    list_of_name[0] = scale
    list_of_name[1] = tab

    for k in range (0,len(fileName)):
        with open(fileName[k], 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            first_line = True
            for row in plots:
                if first_line:
                    for column in range(0, len(row)):
                        for i in range(0, len(list_of_name)):
                            if list_of_name[i] == row[column]:
                                column_number[i] = column
                    first_line = False
                else:
                    for i in range(0,2):
                        if k == 0:
                            if i == 0:
                                array[i].append((float(row[column_number[i]])))
                            else:
                                array[i].append((float(row[column_number[i]])))
                        else:
                            if i == 0:
                                array2[i].append((float(row[column_number[i]])))
                            else:
                                array2[i].append((float(row[column_number[i]])))
    print(column_number)
    print(array)
    print(array2)
    pp = PdfPages(resultFileName)

    plt.figure()
    color = 'b'
    i = 1
    if len(array[i])>0:
        ymax = max(array[i])
        xpos = array[i].index(ymax)
        plt.plot(array[0], array[i],color)
    if len(array2[i])>0:
        color = 'r'
        ymax = max(array2[i])
        xpos = array2[i].index(ymax)
        plt.plot(array2[0], array2[i],color)

        plt.xlabel('N step')
        plt.savefig(pp,format='pdf')

    plt.figure()

    pp.close()
    print(resultFileName, " generated")


def get_config_from_name(file):
    try :
        file = file.split(".csv")[0]
        file = file.split("evaluations/")[1]
        config = cg.Configuration.grab(file)
    except FileNotFoundError:
        config = cg.Configuration.grab()
    title = "Monitors : "
    for typeOfMonitor in config.monitors:
        for monitors in typeOfMonitor:
            for monitor in monitors:
                if monitor.active:
                    title += monitor.type + "_" + monitor.name
    rewards = "reward goal : {0} ".format(config.rewards.standard.goal)
    rewards += "/ step : {0} ".format(config.rewards.standard.step)
    rewards += "/ death : {0} ".format(config.rewards.standard.death)
    return title + "\n" + rewards


def autoPlot(scale,tab):
    csvFileQueue = []
    for csvFile in glob.glob("evaluations/*.csv"):
        csvFileQueue.append(csvFile)
        name = csvFile
        random_number = randint(0,999999)
        name = name.replace(".csv",str(random_number))
        name += str(".pdf")
        name = name.replace("evaluations/","results/")
    plot_result(scale,tab,csvFileQueue,name)


scale = "N_goal_reached"
second_graph = "N_step_AVG"
tab = (second_graph)
autoPlot(scale, tab)