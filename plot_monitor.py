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
"""
File used to create a graph from a csv file and the name of the columns that need to be used
"""

plt.rcParams["font.family"] = "Times New Roman"


def plot_result(scale, tab, fileNameMon, fileNameNoMon, resultFileName):
    pp = PdfPages(resultFileName)
    print(fileNameMon[0])
    title = get_config_from_name(fileNameMon[0])

    array_mon = [[[] for i in range(0, len(tab) * 2 + 1)] for e in range(len(fileNameMon))]
    array_nomon = [[[] for i in range(0, len(tab) * 2 + 1)] for e in range(len(fileNameNoMon))]
    mean_array_mon = [[] for i in range(0, len(tab) * 2 + 1)]
    mean_array_nomon = [[] for i in range(0, len(tab) * 2 + 1)]
    column_number = [0 for i in range(0, len(tab) * 2 + 1)]
    list_of_name = ["" for i in range(0, len(tab) * 2 + 1)]
    list_of_name[0] = scale
    cpt = 1
    last_mean_mon = [float(0) for i in range(0, 22)]
    last_mean_nomon = [float(0) for i in range(0, 22)]
    one_process_max = 0
    all_process_max = 0
    test = False

    step_mon = len(fileNameMon) // 5
    step_nomon = len(fileNameNoMon) // 5

    for x, y, z in tab:
        list_of_name[cpt] = x
        cpt += 1
        list_of_name[cpt] = y
        cpt += 1
    for t in range(0, len(fileNameMon)):
        with open(fileNameMon[t], 'r') as csvfile:
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
                        array_mon[t][i].append((float(row[column_number[i]])))
                if test is not True:
                    if row[6] == "1.0":
                        one_process_max += float(row[0])
                        test = True
            for k in range(len(last_mean_mon)):
                last_mean_mon[k] += float(row[k])
        test = False

    one_process_max = one_process_max / len(fileNameMon)
    print("Monitor: one_process_max : ", one_process_max)

    for t in range(0, len(array_mon)):
        pmax = max(array_mon[t][-2])
        pos = array_mon[t][-2].index(pmax)
        all_process_max += array_mon[t][0][pos]
    all_process_max = all_process_max / len(array_mon)
    print("Monitor: all_process_max : ", all_process_max)
    for k in range(len(last_mean_mon)):
        last_mean_mon[k] = last_mean_mon[k] / len(fileNameMon)
    print("Monitor: ", last_mean_mon)

    for t in range(0, len(mean_array_mon[0])):
        for j in range(len(mean_array_mon)):
            mean_array_mon[j][t] = mean_array_mon[j][t][0]

    one_process_max = 0
    all_process_max = 0

    for t in range(0, len(fileNameNoMon)):
        with open(fileNameNoMon[t], 'r') as csvfile:
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
                        array_nomon[t][i].append((float(row[column_number[i]])))
                if test is not True:
                    if row[6] == "1.0":
                        one_process_max += float(row[0])
                        test = True
            for k in range(len(last_mean_nomon)):
                last_mean_nomon[k] += float(row[k])
        test = False

    one_process_max = one_process_max / len(fileNameNoMon)
    print("No Monitor: one_process_max : ", one_process_max)

    for t in range(0, len(array_nomon)):
        pmax = max(array_nomon[t][-2])
        pos = array_nomon[t][-2].index(pmax)
        all_process_max += array_nomon[t][0][pos]
    all_process_max = all_process_max / len(array_nomon)
    print("No Monitor: all_process_max : ", all_process_max)
    for k in range(len(last_mean_nomon)):
        last_mean_nomon[k] = last_mean_nomon[k] / len(fileNameNoMon)
    print("No Monitor: ", last_mean_nomon)

    for t in range(0, len(mean_array_nomon[0])):
        for j in range(len(mean_array_nomon)):
            mean_array_nomon[j][t] = mean_array_nomon[j][t][0]

    i = 1

    for x, y, z in tab:
        if x == "N_step_AVG" or x == "N_death" or x == "Reward_mean":
            plt.figure()
            for t in range(0, 5):
                if len(array_mon[t * step_mon][i]) > 0:
                    color = 'r'
                    plt.plot(array_mon[t * step_mon][0], array_mon[t * step_mon][i], color, linewidth=1,
                             label=x + "_monitor")

                if len(array_nomon[t * step_nomon][i]) > 0:
                    color = 'b'
                    plt.plot(array_nomon[t * step_mon][0], array_nomon[t * step_mon][i], color, linewidth=1,
                             label=x + "no_monitor")
                """
                if z:
                    area_top = []
                    area_bot = []
                    for k in range(len(array_mon[t*step_mon][i + 1])):
                        area_top.append(array_mon[t*step_mon][i][k] + array_mon[t*step_mon][i + 1][k])
                        area_bot.append(array_mon[t*step_mon][i][k] - array_mon[t*step_mon][i + 1][k])
                    plt.fill_between(array_mon[t*step_mon][0], area_bot, area_top, color="red", alpha=0.4)

                    area_top = []
                    area_bot = []
                    for k in range(len(array_nomon[t*step_nomon][i + 1])):
                        area_top.append(array_nomon[t*step_nomon][i][k] + array_nomon[t*step_nomon][i + 1][k])
                        area_bot.append(array_nomon[t*step_nomon][i][k] - array_nomon[t*step_nomon][i + 1][k])
                    plt.fill_between(array_nomon[t*step_nomon][0], area_bot, area_top, color="skyblue", alpha=0.4)
                    """
                # plt.legend()
                # plt.xlabel('N Updates')
                # plt.title(title)
            plt.savefig(pp, format='pdf')

        if y == "N_goal_reached":
            plt.figure()
            for t in range(0, 5):
                if len(array_mon[t * step_mon][i + 1]) > 0:
                    color = 'r'
                    plt.plot(array_mon[t * step_mon][0], array_mon[t * step_mon][i + 1], color, linewidth=1,
                             label=x + "_monitor")
                if len(array_nomon[t * step_nomon][i + 1]) > 0:
                    color = 'b'
                    plt.plot(array_nomon[t * step_nomon][0], array_nomon[t * step_nomon][i + 1], color, linewidth=1,
                             label=x + "no_monitor")
                # plt.legend()
                # plt.xlabel('N Updates')
                # plt.title(title)
            plt.savefig(pp, format='pdf')

        i += 2

    plt.figure()
    Name = fileNameMon[0]
    Name = Name.replace("_0", "")
    img = get_image_from_name("configurations/*", Name)
    if img is not None:
        if "main" in img:
            screenHelper.main()
        img = plt.imread(img)
        plt.imshow(img)
        plt.savefig(pp, format='pdf')
    pp.close()
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


def get_image_from_name(path, my_file):
    for file in glob.glob(path):
        if ".json" in file:
            file = file.split("configurations/")[1]
            file = file.split(".json")[0]
            try:
                config = cg.Configuration.grab(file)
            except FileNotFoundError:
                config = cg.Configuration.grab()
            my_file = my_file.replace(".csv", "")

            number_of_slash = 0
            for i in range(len(my_file)):
                if my_file[i] == '/':
                    number_of_slash += 1
            pos = 0
            for j in range(number_of_slash):
                pos = my_file.find('/', pos)
            my_file = my_file[pos + 1:]
            if config.config_name == my_file:
                if "randoms" in path:
                    return "results/screens/randoms/" + config.env_name + ".png"
                if "crafted" in path:
                    return "results/screens/crafted/" + config.env_name + ".png"
                return "results/screens/" + config.env_name + ".png"
    if "crafted" not in path and "randoms" not in path:
        return get_image_from_name("configurations/crafted/*", my_file)
    elif "randoms" not in path:
        return get_image_from_name("configurations/randoms/*", my_file)
    else:
        return None


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


def create_all_images(path):
    for file in glob.glob(path):
        # Folder except rewards and environments
        if "." not in file and "rewards" not in file and "environments" not in file:
            create_all_images(file + "/*")
        elif ".json" in file:
            # image need to be created
            file = file.split("configurations/")[1]
            file = file.split(".json")[0]
            if not check_if_image_already_exist(file):
                screenHelper.main(file)


def check_if_image_already_exist(path):
    config = cg.Configuration.grab(path)
    folder = ""
    if "crafted" in path:
        folder = "crafted/"
    elif "randoms" in path:
        folder = "randoms/"
    path = path.replace(path, "results/screens/" + folder + config.env_name + ".png")
    path = Path(path)
    if path.exists():
        return True
    return False


create_all_images("configurations/*")
print("all images created")

scale = "N_updates"
first_graph = ("N_step_AVG", "N_goal_reached", False)
second_graph = ("N_death", "N_saved", False)
third_graph = ("Reward_mean", "Reward_std", True)
tab = (first_graph, second_graph, third_graph)
autoPlot(scale, tab)
