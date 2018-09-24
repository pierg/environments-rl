import matplotlib
import os

matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import glob
from random import randint

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 10})

# Data
eval_name = []
envelope = []

N_updates = []
N_timesteps = []
Reward_mean = []
Reward_median = []
Reward_min = []
Reward_max = []
Reward_std = []
Entropy = []
Value_loss = []
Action_loss = []
N_violation_avg = []
N_goals_avg = []
N_died_avg = []
N_end_avg = []
N_step_goal_avg = []
eval_name = []
envelope = []


def extract_all_data_from_csv(csv_folder_abs_path):
    for file_name in os.listdir(csv_folder_abs_path):
        if "a2c" in file_name and ".csv" in file_name:
            print("CsvName : ", file_name)
            file_eval_name = file_name.replace(".csv", "")
            N_updates.append(extract_array("N_updates", csv_folder_abs_path + "/" + file_name))
            N_timesteps.append(extract_array("N_timesteps", csv_folder_abs_path + "/" + file_name))
            Reward_mean.append(extract_array("Reward_mean", csv_folder_abs_path + "/" + file_name))
            Reward_median.append(extract_array("Reward_median", csv_folder_abs_path + "/" + file_name))
            Reward_min.append(extract_array("Reward_min", csv_folder_abs_path + "/" + file_name))
            Reward_max.append(extract_array("Reward_max", csv_folder_abs_path + "/" + file_name))
            Reward_std.append(extract_array("Reward_std", csv_folder_abs_path + "/" + file_name))
            Entropy.append(extract_array("Entropy", csv_folder_abs_path + "/" + file_name))
            Value_loss.append(extract_array("Value_loss", csv_folder_abs_path + "/" + file_name))
            Action_loss.append(extract_array("Action_loss", csv_folder_abs_path + "/" + file_name))
            N_violation_avg.append(extract_array("N_violation_avg", csv_folder_abs_path + "/" + file_name))
            N_goals_avg.append(extract_array("N_goals_avg", csv_folder_abs_path + "/" + file_name))
            N_died_avg.append(extract_array("N_died_avg", csv_folder_abs_path + "/" + file_name))
            N_end_avg.append(extract_array("N_end_avg", csv_folder_abs_path + "/" + file_name))
            N_step_goal_avg.append(extract_array("N_step_goal_avg", csv_folder_abs_path + "/" + file_name))
            eval_name.append(file_eval_name)
            envelope.append(extract_array("envelope", csv_folder_abs_path + "/" + file_name)[0])


def extract_array(label, csv_file):
    """
    Extract values from csv
    :param label: label of the data in the csv_file
    :param csv_file: full path of the csv_file
    :return: array with all the values under 'label'
    """
    values = []
    with open(csv_file, 'r') as current_csv:
        plots = csv.reader(current_csv, delimiter=',')
        first_line = True
        label_index = -1
        for row in plots:
            if first_line:
                for column in range(0, len(row)):
                    if row[column] == label:
                        label_index = column
                        break
                first_line = False
            else:
                if label_index == -1:
                    assert False, "error label not found '%s'" % label
                try:
                    values.append(float(row[label_index]))
                except ValueError:
                    values.append(row[label_index])

    return values


def single_line_plot(x, y, x_label, y_label, ys_sem=0, title=""):
    """
    Plots y on x
    :param x: array of values rappresenting the x, scale
    :param y: array containing the data corresponding to x
    :param x_label: label of x
    :param y_labels: label of y
    :param y_sem: (optional) standard error mean, it adds as translucent area around the y
    :return: matplot figure, it can then be added to a pdf
    """
    x_size = 20
    y_size = 2
    figure = plt.figure(num=None, figsize=(x_size, y_size), dpi=80, facecolor='w', edgecolor='k')
    plt.suptitle(title)
    plt.grid(True)

    plt.plot(x, y, linewidth=0.5)
    if ys_sem != 0 and len(y) != 0:
        area_top = [y[0]]
        area_bot = [y[0]]
        for k in range(1, len(y)):
            area_bot.append(y[k] - ys_sem[k - 1])
            area_top.append(y[k] + ys_sem[k - 1])
        plt.fill_between(x, area_bot, area_top, color="skyblue", alpha=0.4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    return figure


def multi_line_plot(x, ys, x_label, y_labels, ys_sem=0, title=""):
    """
    Plots all the elements in the y[0], y[1]...etc.. as overlapping lines on on the x
    :param x: array of values rappresenting the x, scale
    :param ys: multi-dimensional array containing the data of all the plots to be overlapped on the same figure
    :param x_label: label of x
    :param y_labels: labels of ys
    :param ys_sem: (optional) standard error mean, it adds as translucent area around the ys
    :return: matplot figure, it can then be added to a pdf
    """
    figure = plt.figure()
    plt.suptitle(title)
    plt.grid(True)

    for k in range(len(ys)):
        plt.plot(x, ys[k], label=y_labels[k])
    plt.legend()

    return figure


def multi_figures_plot(x, ys, x_label, y_labels, ys_sem=0, title=""):
    """
    Plots all the elements in the y[0], y[1]...etc.. as lines on on the x in different figures next to each other
    (one x in the bottom and multiple y "on top" of each other but not overlapping)
    :param x: array of values rappresenting the x, scale
    :param ys: multi-dimensional array containing the data of all the plots to be overlapped on the same figure
    :param x_label: label of x
    :param y_labels: labels of ys
    :param ys_sem: (optional) standard error mean, it adds as translucent area around the ys
    :return: matplot figure, it can then be added to a pdf
    """
    x_size = 20
    y_size = len(y_labels) * 2
    figure = plt.figure(num=None, figsize=(x_size, y_size), dpi=80, facecolor='w', edgecolor='k')
    plt.suptitle(title)
    plt.grid(True)

    ax_to_send = figure.subplots(nrows=len(ys), ncols=1)
    if len(ys) == 1:
        return single_line_plot(x, ys[0], x_label, y_labels[0], ys_sem)
    for k in range(len(ys)):
        ax_to_send[k].plot(x, ys[k], linewidth=1)
        ax_to_send[k].set_xlabel(x_label)
        ax_to_send[k].set_ylabel(y_labels[k])
        if ys_sem != 0:
            if ys_sem[k] != 0 and len(ys[k]) != 0:
                area_top = [ys[k][0]]
                area_bot = [ys[k][0]]
                for j in range(1, len(ys[k])):
                    area_bot.append(ys[k][j] - ys_sem[k][j - 1])
                    area_top.append(ys[k][j] + ys_sem[k][j - 1])
                ax_to_send[k].fill_between(x, area_bot, area_top, color="skyblue", alpha=0.4)
        ax_to_send[k].axes.get_xaxis().set_visible(False)
    ax_to_send[k].axes.get_xaxis().set_visible(True)

    return figure


def plot():
    current_directory = os.path.abspath(os.path.dirname(__file__))
    extract_all_data_from_csv(current_directory)
    for i in range(len(N_updates)):
        title = "envelope : " + str(envelope[i])
        figure_1 = multi_figures_plot(N_updates[i],
                                      [N_goals_avg[i],
                                       N_step_goal_avg[i]
                                       ], 'N_updates', ['N goals reached (avg)',
                                                        'steps to goal (avg)'
                                                        ], title=title)

        figure_2 = multi_figures_plot(N_updates[i],
                                      [N_died_avg[i],
                                       N_end_avg[i],
                                       N_violation_avg[i]
                                       ], 'N_updates', ['N deaths (avg)',
                                                        'N ended (avg)',
                                                        'N violations (avg)'
                                                        ])

        figure_3 = single_line_plot(N_updates[i],
                                    Reward_mean[i],
                                    'N_updates',
                                    'reward mean and sem',
                                    Reward_std[i])

        if envelope[i] == "True":
            Name = eval_name[i] + ".pdf"
        else:
            Name = eval_name[i] + ".pdf"

        print("PdfName : ", Name)

        pdf = PdfPages(current_directory + "/" + Name)

        pdf.savefig(figure_3)
        pdf.savefig(figure_1)
        pdf.savefig(figure_2)

        pdf.close()


if __name__ == "__main__":
    plot()
