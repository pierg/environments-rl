import matplotlib
import os

matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import glob
from random import randint

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 15})


# Data
n_timesteps = []
n_step_AVG = []
n_goal_reached = []
n_violation = []
n_death = []
reward_mean = []
reward_std = []


def extract_all_data_from_csv(csv_folder_abs_path):
    for csv_file_name in os.listdir(csv_folder_abs_path):
        if "a2c" in csv_file_name and ".csv" in csv_file_name:
            print("CsvName : ", csv_file_name)
            n_timesteps.append(extract_array("N_timesteps", csv_folder_abs_path + "/" + csv_file_name))
            n_step_AVG.append(extract_array("N_step_AVG", csv_folder_abs_path + "/" + csv_file_name))
            n_goal_reached.append(extract_array("N_goal_reached", csv_folder_abs_path + "/" + csv_file_name))
            n_violation.append(extract_array("N_violation", csv_folder_abs_path + "/" + csv_file_name))
            n_death.append(extract_array("N_death", csv_folder_abs_path + "/" + csv_file_name))
            reward_mean.append(extract_array("Reward_mean", csv_folder_abs_path + "/" + csv_file_name))
            reward_std.append(extract_array("Reward_std", csv_folder_abs_path + "/" + csv_file_name))


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
                values.append(float(row[label_index]))

    return values


def single_line_plot(x, y, x_label, y_label, ys_sem = 0):
    """
    Plots y on x
    :param x: array of values rappresenting the x, scale
    :param y: array containing the data corresponding to x
    :param x_label: label of x
    :param y_labels: label of y
    :param y_sem: (optional) standard error mean, it adds as translucent area around the y
    :return: matplot figure, it can then be added to a pdf
    """
    figure = plt.figure()
    plt.plot(x, y, linewidth=0.5)

    if ys_sem != 0 and len(y) !=0:
        area_top = [y[0]]
        area_bot = [y[0]]
        for k in range(1, len(y)):
            area_bot.append(y[k] - ys_sem[k - 1])
            area_top.append(y[k] + ys_sem[k - 1])
        plt.fill_between(x, area_bot, area_top, color="skyblue", alpha=0.4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    return figure

def multi_line_plot(x, ys, x_label, y_labels, ys_sem=0):
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
    for k in range(len(ys)):
        plt.plot(x, ys[k],label= y_labels[k])
    plt.legend()

    return figure


def multi_figures_plot(x, ys, x_label, y_labels, ys_sem=0):
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
    x_size = 10
    y_size = len(y_labels)*2
    figure = plt.figure(num=None, figsize=(x_size, y_size), dpi=80, facecolor='w', edgecolor='k')
    ax_to_send = figure.subplots(nrows = len(ys), ncols=1)
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
    for i in range(len(n_timesteps)):

        figure_1 = multi_figures_plot(n_timesteps[i],
                           [n_step_AVG[i],
                            n_goal_reached[i]
                             ], 'N_timesteps', ['N_step_AVG',
                                                 'N_goal_reached'
                                                    ])

        figure_2 = multi_figures_plot(n_timesteps[i],
                                      [n_death[i],
                                       n_violation[i]
                                       ], 'N_timesteps', ['N_death',
                                                          'N_violation'
                                                          ])

        figure_3 = multi_figures_plot(n_timesteps[i],
                                      [reward_mean[i],
                                       reward_std[i]
                                       ], 'N_timesteps', ['Reward_mean',
                                                          'Reward_std'
                                                          ],[reward_std[i],0])

        Name = "a2c_experience_[" + str(i) + "].pdf"
        print("PdfName : ", Name)


        pdf = PdfPages(current_directory + "/" + Name)

        pdf.savefig(figure_1)
        pdf.savefig(figure_2)
        pdf.savefig(figure_3)

        pdf.close()



if __name__ == "__main__":
    plot()
