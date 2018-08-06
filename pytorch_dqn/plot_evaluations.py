import matplotlib
import os

matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import glob
from random import randint
import configurations.config_grabber as cg

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 15})


# Data
# Episodes
epi_episode_idx = []
epi_n_steps_goal = []
epi_last_epsilon = []
epi_n_violations = []
epi_n_deaths = []
epi_reward_cum = []

# Frames
frm_frame_idx = []
frm_reward_mean = []
frm_reward_sem = []
frm_reward_cum = []


def extract_all_data_from_csv(csv_folder_abs_path):
    for csv_file_name in os.listdir(csv_folder_abs_path):
        if "epi" in csv_file_name:
            print("CsvName : ", csv_file_name)
            epi_episode_idx.append(extract_array("episode_idx", csv_folder_abs_path + "/" + csv_file_name))
            epi_n_steps_goal.append(extract_array("n_steps_goal", csv_folder_abs_path + "/" + csv_file_name))
            epi_last_epsilon.append(extract_array("last_epsilon", csv_folder_abs_path + "/" + csv_file_name))
            epi_n_violations.append(extract_array("n_violations", csv_folder_abs_path + "/" + csv_file_name))
            epi_n_deaths.append(extract_array("n_deaths", csv_folder_abs_path + "/" + csv_file_name))
            epi_reward_cum.append(extract_array("reward_cum", csv_folder_abs_path + "/" + csv_file_name))

        elif "frm" in csv_file_name:
            print("CsvName : ", csv_file_name)
            frm_frame_idx.append(extract_array("frame_idx", csv_folder_abs_path + "/" + csv_file_name))
            frm_reward_mean.append(extract_array("reward_mean", csv_folder_abs_path + "/" + csv_file_name))
            frm_reward_sem.append(extract_array("reward_sem", csv_folder_abs_path + "/" + csv_file_name))
            frm_reward_cum.append(extract_array("reward_cum", csv_folder_abs_path + "/" + csv_file_name))


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
    plt.plot(x, y, linewidth=1)

    if ys_sem != 0:
        area_top = []
        area_bot = []
        for k in range(len(y)):
            area_bot.append(y[k] - ys_sem[k - 1])
            area_top.append(y[k] + ys_sem[k - 1])
        plt.fill_between(x, area_bot, area_top, color="skyblue", alpha=0.4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    return figure

# TODO
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
    figure = plt.figure()
    ax_to_send = figure.subplots(nrows = len(ys), ncols=1)
    if len(ys) == 1:
        return single_line_plot(x, ys[0], x_label, y_labels[0], ys_sem[0])
    else:
        for k in range(len(ys)):
            ax_to_send[k].plot(x, ys[k], linewidth=1)
            ax_to_send[k].set_xlabel(x_label)
            ax_to_send[k].set_ylabel(y_labels[k])
            if ys_sem != 0:
                if ys_sem[k] != 0:
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
    extract_all_data_from_csv(os.path.abspath(os.path.dirname(__file__) + "/../evaluations/"))

    figure_episodes = multi_figures_plot(epi_episode_idx[0],
                       [epi_n_steps_goal[0],
                        epi_last_epsilon[0],
                        epi_n_violations[0],
                        epi_reward_cum[0]], 'epi_episode_idx', ['n_steps_goal',
                                             'last_epsilon',
                                             'n_violations',
                                             'reward_cum'])

    figure_frames = multi_figures_plot(frm_frame_idx[0],
                       [frm_reward_mean[0],
                        frm_reward_cum[0]], 'frm_frame_idx',['n_steps_goal',
                                             'reward_cum'],[frm_reward_sem[0], 0])

    # TODO: save the 2 figures as 2 pages in a single pdf and save the pdf in the evaluation folder
    Name = "dqn_experience_"+ str(randint(0,999999))+ ".pdf"
    print("PdfName : ", Name)

    os.chdir(os.path.dirname(__file__) + "/../evaluations/")
    pdf = PdfPages(Name)

    pdf.savefig(figure_episodes)
    pdf.savefig(figure_frames)
    pdf.close()



if __name__ == "__main__":
    plot()
