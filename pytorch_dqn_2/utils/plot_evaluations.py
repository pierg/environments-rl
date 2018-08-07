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
            epi_episode_idx.append(extract_array("episode_idx", csv_file_name))
            epi_n_steps_goal.append(extract_array("n_steps_goal", csv_file_name))
            epi_last_epsilon.append(extract_array("last_epsilon", csv_file_name))
            epi_n_violations.append(extract_array("n_violations", csv_file_name))
            epi_n_deaths.append(extract_array("n_deaths", csv_file_name))
            epi_reward_cum.append(extract_array("reward_cum", csv_file_name))

        elif "frm" in csv_file_name:
            frm_frame_idx.append(extract_array("frame_idx", csv_file_name))
            frm_reward_mean.append(extract_array("reward_mean", csv_file_name))
            frm_reward_sem.append(extract_array("reward_sem", csv_file_name))
            frm_reward_cum.append(extract_array("reward_cum", csv_file_name))


# TODO
def extract_array(label, csv_file):
    """
    Extract values from csv
    :param label: label of the data in the csv_file
    :param csv_file: full path of the csv_file
    :return: array with all the values under 'label'
    """
    values = []

    return values


# TODO
def single_line_plot(x, y, x_label, y_label, ys_sem=0):
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

    return figure

# TODO
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

    return figure


def plot():
    extract_all_data_from_csv(os.path.abspath(os.path.dirname(__file__) + "/../evaluations/"))

    figure_episodes = multi_figures_plot(epi_episode_idx[0],
                       [epi_n_steps_goal[0],
                        epi_last_epsilon[0],
                        epi_n_violations[0],
                        epi_reward_cum[0]], ['n_steps_goal',
                                             'last_epsilon',
                                             'n_violations',
                                             'reward_cum'])

    figure_frames = multi_figures_plot(frm_frame_idx[0],
                       [frm_reward_mean[0],
                        frm_reward_cum[0]], ['n_steps_goal',
                                             'reward_cum'], [frm_reward_sem[0], 0])

    # TODO: save the 2 figures as 2 pages in a single pdf and save the pdf in the evaluation folder
    plt.savefig(figure_episodes, format='pdf')
    plt.savefig(figure_frames, format='pdf')


if __name__ == "__main__":
    plot()
