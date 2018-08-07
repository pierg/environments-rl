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

plt.savefig("foo.pdf", bbox_inches="tight", pad_inches=0)
plt.rcParams["font.family"] = "Times New Roman"

"""
File used to create a graph from a csv file and the name of the columns that need to be used
"""


def plot_result(scale, tab, fileNameMo, fileNameNoMo, resultFileName):
    pp_mo = PdfPages(resultFileName)
    resultFileName_nomo = resultFileName.replace(".pdf", "_nomonitor.pdf")
    print(resultFileName_nomo, "   ", resultFileName)
    pp_nomo = PdfPages(resultFileName_nomo)
    title = get_config_from_name(fileNameMo[0])

    array_mo = [[[] for i in range(0, len(tab) * 2 + 1)] for e in range(len(fileNameMo))]
    array_nomo = [[[] for i in range(0, len(tab) * 2 + 1)] for e in range(len(fileNameMo))]
    mean_array_mo = [[] for i in range(0, len(tab) * 2 + 1)]
    mean_array_nomo = [[] for i in range(0, len(tab) * 2 + 1)]
    column_number = [0 for i in range(0, len(tab) * 2 + 1)]
    list_of_name = ["" for i in range(0, len(tab) * 2 + 1)]
    list_of_name[0] = scale
    cpt = 1
    last_mean_mo = [float(0) for i in range(0, 22)]
    last_mean_nomo = [float(0) for i in range(0, 22)]
    one_process_max = 0
    all_process_max = 0
    test = False

    for x, y, z in tab:
        list_of_name[cpt] = x
        cpt += 1
        list_of_name[cpt] = y
        cpt += 1
    for t in range(0, len(fileNameMo)):
        with open(fileNameMo[t], 'r') as csvfile:
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
                    for i in range(0, len(tab) * 2 + 1):
                        array_mo[t][i].append((float(row[column_number[i]])))
                if test is not True:
                    if row[6] == "1.0":
                        one_process_max += float(row[0])
                        test = True
            for k in range(len(last_mean_mo)):
                last_mean_mo[k] += float(row[k])
            for i in range(0, len(tab) * 2 + 1):
                for j in range(0, len(array_mo[t][i])):
                    if j < len(mean_array_mo[i]) and len(mean_array_mo[i]) != 0:
                        mean_array_mo[i][j][0] = (mean_array_mo[i][j][0] * mean_array_mo[i][j][1] + array_mo[t][i][
                            j]) / (mean_array_mo[i][j][1] + 1)
                        mean_array_mo[i][j][1] += 1
                    else:
                        mean_array_mo[i].append([array_mo[t][i][j], 1])
        test = False

    one_process_max = one_process_max / len(fileNameMo)
    print("one_process_max : ", one_process_max)

    for t in range(0, len(array_mo)):
        pmax = max(array_mo[t][-2])
        pos = array_mo[t][-2].index(pmax)
        all_process_max += array_mo[t][0][pos]
    all_process_max = all_process_max / len(array_mo)
    print("all_process_max : ", all_process_max)
    for k in range(len(last_mean_mo)):
        last_mean_mo[k] = last_mean_mo[k] / len(fileNameMo)
    print(last_mean_mo)

    for t in range(0, len(mean_array_mo[0])):
        for j in range(len(mean_array_mo)):
            mean_array_mo[j][t] = mean_array_mo[j][t][0]

    plt.figure()
    for t in range(0, len(fileNameMo)):
        if len(array_mo[t][1]) > 0:
            color = 0
            ymax = max(array_mo[t][1])
            xpos = array_mo[t][1].index(ymax)
            xmax = array_mo[t][0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(array_mo[t][0], array_mo[t][1], color + t * 5, label=list_of_name[1])

    plt.ylabel(str(list_of_name[1]))

    plt.savefig(pp_mo, format='pdf')

    plt.figure()
    for t in range(0, len(fileNameMo)):
        if len(array_mo[t][2]) > 0:
            color = 0
            ymax = max(array_mo[t][2])
            xpos = array_mo[t][2].index(ymax)
            xmax = array_mo[t][0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(array_mo[t][0], array_mo[t][2], color + t * 5, label=list_of_name[2])

    plt.ylabel(str(list_of_name[2]))

    plt.savefig(pp_mo, format='pdf')

    plt.figure()
    if len(mean_array_mo[2]) > 0:
        ymax = max(mean_array_mo[2])
        xpos = mean_array_mo[2].index(ymax)
        xmax = mean_array_mo[0][xpos]
        ymax = float("{0:.1f}".format(ymax))
        plt.plot(mean_array_mo[0], mean_array_mo[2], 'y', linewidth=2.5, label=list_of_name[2] + "_mean")

    if len(mean_array_mo[1]) > 0:
        ymax = max(mean_array_mo[1])
        xpos = mean_array_mo[1].index(ymax)
        xmax = mean_array_mo[0][xpos]
        ymax = float("{0:.1f}".format(ymax))
        plt.plot(mean_array_mo[0], mean_array_mo[1], 'r', linewidth=2.5, label=list_of_name[1] + "_mean")

    plt.legend()

    plt.savefig(pp_mo, format='pdf')

    i = 1
    for x, y, z in tab:
        if x == list_of_name[1]:
            i += 2
            continue
        plt.figure()
        for t in range(0, len(fileNameMo)):
            color = 'g'
            if len(array_mo[t][i]) > 0:
                ymax = max(array_mo[t][i])
                xpos = array_mo[t][i].index(ymax)
                xmax = array_mo[t][0][xpos]
                ymax = float("{0:.1f}".format(ymax))
                if t == 0:
                    plt.plot(array_mo[t][0], array_mo[t][i], color, label=x)
                else:
                    plt.plot(array_mo[t][0], array_mo[t][i], color)

            if len(array_mo[t][i + 1]) > 0:
                color = 'b'
                ymax = max(array_mo[t][i + 1])
                xpos = array_mo[t][i + 1].index(ymax)
                xmax = array_mo[t][0][xpos]
                ymax = float("{0:.1f}".format(ymax))
                if t == 0:
                    plt.plot(array_mo[t][0], array_mo[t][i + 1], color, label=y)
                else:
                    plt.plot(array_mo[t][0], array_mo[t][i + 1], color)

            if z:
                area_top = []
                area_bot = []
                for k in range(0, len(array_mo[t][i + 1])):
                    area_top.append(array_mo[t][i][k] + array_mo[t][i + 1][k])
                    area_bot.append(array_mo[t][i][k] - array_mo[t][i + 1][k])
                plt.fill_between(array_mo[t][0], area_bot, area_top, color="skyblue", alpha=0.4)

        color = 'r'
        if len(mean_array_mo[i]) > 0:
            ymax = max(mean_array_mo[i])
            xpos = mean_array_mo[i].index(ymax)
            xmax = mean_array_mo[0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(mean_array_mo[0], mean_array_mo[i], color, linewidth=2.5, label=x + "_mean")

        if len(mean_array_mo[i + 1]) > 0:
            color = 'y'
            ymax = max(mean_array_mo[i + 1])
            xpos = mean_array_mo[i + 1].index(ymax)
            xmax = mean_array_mo[0][xpos]
            ymax = float("{0:.1f}".format(ymax))

        if z:
            area_top = []
            area_bot = []
            for k in range(0, len(mean_array_mo[i + 1])):
                area_top.append(mean_array_mo[i][k] + mean_array_mo[i + 1][k])
                area_bot.append(mean_array_mo[i][k] - mean_array_mo[i + 1][k])
            plt.fill_between(mean_array_mo[0], area_bot, area_top, color="skyblue", alpha=0.4)

        i += 2

        plt.legend()
        plt.savefig(pp_mo, format='pdf')

    plt.figure()
    Name = fileNameMo[0]
    Name = Name.replace("_0", "")
    pp_mo.close()
    print(resultFileName, " generated")

    for t in range(0, len(fileNameNoMo)):
        with open(fileNameNoMo[t], 'r') as csvfile:
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
                    for i in range(0, len(tab) * 2 + 1):
                        array_nomo[t][i].append((float(row[column_number[i]])))
                if test is not True:
                    if row[6] == "1.0":
                        one_process_max += float(row[0])
                        test = True
            for k in range(len(last_mean_nomo)):
                last_mean_nomo[k] += float(row[k])
            for i in range(0, len(tab) * 2 + 1):
                for j in range(0, len(array_nomo[t][i])):
                    if j < len(mean_array_nomo[i]) and len(mean_array_nomo[i]) != 0:
                        mean_array_nomo[i][j][0] = (mean_array_nomo[i][j][0] * mean_array_nomo[i][j][1] +
                                                    array_nomo[t][i][j]) / (mean_array_nomo[i][j][1] + 1)
                        mean_array_nomo[i][j][1] += 1
                    else:
                        mean_array_nomo[i].append([array_nomo[t][i][j], 1])
        test = False

    one_process_max = one_process_max / len(fileNameNoMo)
    print("one_process_max : ", one_process_max)

    for t in range(0, len(array_nomo)):
        if len(array_nomo[t][2]) > 0:
            pmax = max(array_nomo[t][-2])
            pos = array_nomo[t][-2].index(pmax)
            all_process_max += array_nomo[t][0][pos]
    all_process_max = all_process_max / len(array_nomo)
    print("all_process_max : ", all_process_max)
    for k in range(len(last_mean_nomo)):
        last_mean_nomo[k] = last_mean_mo[k] / len(fileNameMo)
    print(last_mean_nomo)

    for t in range(0, len(mean_array_nomo[0])):
        for j in range(len(mean_array_nomo)):
            mean_array_nomo[j][t] = mean_array_nomo[j][t][0]

    plt.figure()
    for t in range(0, len(fileNameNoMo)):
        if len(array_nomo[t][1]) > 0:
            color = 0
            ymax = max(array_nomo[t][1])
            xpos = array_nomo[t][1].index(ymax)
            xmax = array_nomo[t][0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(array_nomo[t][0], array_nomo[t][1], color + t * 5, label=list_of_name[1])

    plt.savefig(pp_nomo, format='pdf')

    plt.figure()
    for t in range(0, len(fileNameNoMo)):
        if len(array_nomo[t][2]) > 0:
            color = 0
            ymax = max(array_nomo[t][2])
            xpos = array_nomo[t][2].index(ymax)
            xmax = array_nomo[t][0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(array_nomo[t][0], array_nomo[t][2], color + t * 5, label=list_of_name[2])

    plt.savefig(pp_nomo, format='pdf')

    plt.figure()
    if len(mean_array_nomo[2]) > 0:
        ymax = max(mean_array_nomo[2])
        xpos = mean_array_nomo[2].index(ymax)
        xmax = mean_array_nomo[0][xpos]
        ymax = float("{0:.1f}".format(ymax))
        plt.plot(mean_array_nomo[0], mean_array_nomo[2], 'y', linewidth=2.5, label=list_of_name[2] + "_mean")

    if len(mean_array_nomo[1]) > 0:
        ymax = max(mean_array_nomo[1])
        xpos = mean_array_nomo[1].index(ymax)
        xmax = mean_array_nomo[0][xpos]
        ymax = float("{0:.1f}".format(ymax))
        plt.plot(mean_array_nomo[0], mean_array_nomo[1], 'r', linewidth=2.5, label=list_of_name[1] + "_mean")

    plt.savefig(pp_nomo, format='pdf')

    i = 1
    for x, y, z in tab:
        if x == list_of_name[1]:
            i += 2
            continue
        plt.figure()
        for t in range(0, len(fileNameNoMo)):
            color = 'g'
            if len(array_nomo[t][i]) > 0:
                ymax = max(array_nomo[t][i])
                xpos = array_nomo[t][i].index(ymax)
                xmax = array_nomo[t][0][xpos]
                ymax = float("{0:.1f}".format(ymax))
                if t == 0:
                    plt.plot(array_nomo[t][0], array_nomo[t][i], color, label=x)
                else:
                    plt.plot(array_nomo[t][0], array_nomo[t][i], color)
            if len(array_nomo[t][i + 1]) > 0:
                color = 'b'
                ymax = max(array_nomo[t][i + 1])
                xpos = array_nomo[t][i + 1].index(ymax)
                xmax = array_nomo[t][0][xpos]
                ymax = float("{0:.1f}".format(ymax))
                if t == 0:
                    plt.plot(array_nomo[t][0], array_nomo[t][i + 1], color, label=y)
                else:
                    plt.plot(array_nomo[t][0], array_nomo[t][i + 1], color)

            if z:
                area_top = []
                area_bot = []
                for k in range(0, len(array_nomo[t][i + 1])):
                    area_top.append(array_nomo[t][i][k] + array_nomo[t][i + 1][k])
                    area_bot.append(array_nomo[t][i][k] - array_nomo[t][i + 1][k])
                plt.fill_between(array_nomo[t][0], area_bot, area_top, color="skyblue", alpha=0.4)

        color = 'r'
        if len(mean_array_nomo[i]) > 0:
            ymax = max(mean_array_nomo[i])
            xpos = mean_array_nomo[i].index(ymax)
            xmax = mean_array_nomo[0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(mean_array_nomo[0], mean_array_nomo[i], color, linewidth=2.5, label=x + "_mean")

        if len(mean_array_nomo[i + 1]) > 0:
            color = 'y'
            ymax = max(mean_array_nomo[i + 1])
            xpos = mean_array_nomo[i + 1].index(ymax)
            xmax = mean_array_nomo[0][xpos]
            ymax = float("{0:.1f}".format(ymax))
            plt.plot(mean_array_nomo[0], mean_array_nomo[i + 1], color, linewidth=2.5, label=y + "_mean")

        if z:
            area_top = []
            area_bot = []
            for k in range(0, len(mean_array_nomo[i + 1])):
                area_top.append(mean_array_nomo[i][k] + mean_array_nomo[i + 1][k])
                area_bot.append(mean_array_nomo[i][k] - mean_array_nomo[i + 1][k])
            plt.fill_between(mean_array_nomo[0], area_bot, area_top, color="skyblue", alpha=0.4)

        i += 2

        plt.savefig(pp_nomo, format='pdf')

    plt.figure()
    Name = fileNameNoMo[0]
    Name = Name.replace("_0", "")
    pp_nomo.close()
    print(resultFileName, " generated")


def get_config_from_name(file):
    try:
        file = file.split(".csv")[0]
        file = file.replace("evaluations/", "randoms/")
        file = file[:-2]
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


def autoPlot(scale, tab):
    for csvFile in glob.glob("evaluations/*/"):
        monitor = csvFile
        csvFileMon = []
        csvFileNoMon = []
        for csvFile in glob.glob(monitor + "*_0.csv"):
            if csvFile[-8:] == "_2_0.csv":
                csvFileNoMon.append(csvFile)
            else:
                csvFileMon.append(csvFile)
                if len(csvFileMon) == 1:
                    name = csvFile
                    random_number = randint(0, 999999)
                    name = name.replace("_0.csv", "")
                    name = name + (str(random_number))
                    name += str(".pdf")
                    name = name.replace("evaluations/", "results/")
        plot_result(scale, tab, csvFileMon, csvFileNoMon, name)


scale = "N_updates"
first_graph = ("N_step_AVG", "N_goal_reached", False)
second_graph = ("N_death", "N_saved", False)
third_graph = ("Reward_mean", "Reward_std", True)
tab = (first_graph, second_graph, third_graph)
autoPlot(scale, tab)
