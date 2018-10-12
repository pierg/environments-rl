import matplotlib
import os
import sys

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
convergence = []

iterations_number = 10

def max_timesteps(size):
    return size * size * 10000


def respects_criteria(file_name, criteria):
    for word in criteria:
        if word not in file_name:
            return False
    return True


def extract_all_data_from_csv(csv_folder_abs_path, criteria=[]):
    eval_name.clear()
    envelope.clear()
    N_updates.clear()
    N_timesteps.clear()
    Reward_mean.clear()
    Reward_median.clear()
    Reward_min.clear()
    Reward_max.clear()
    Reward_std.clear()
    Entropy.clear()
    Value_loss.clear()
    Action_loss.clear()
    N_violation_avg.clear()
    N_goals_avg.clear()
    N_died_avg.clear()
    N_end_avg.clear()
    N_step_goal_avg.clear()
    eval_name.clear()
    envelope.clear()
    convergence.clear()
    for file_name in os.listdir(csv_folder_abs_path):
        if "a2c" in file_name and ".csv" in file_name and respects_criteria(file_name, criteria):
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
            cut_to_convergence()


def cut_to_convergence():
    count = 0
    size = int(eval_name[-1].split('-')[1].replace('s', ''))
    timesteps = max_timesteps(size)
    for i in range(1, len(N_step_goal_avg[-1])):
        if converged(N_step_goal_avg[-1][i], N_step_goal_avg[-1][i-1], Value_loss[-1][i], Reward_mean[-1][i], Reward_std[-1][i], N_step_goal_avg[-1][i]):
            count += 1
        else:
            count = 0

        if count > 0:
            cut_table(i)
            convergence.append(True)
            return
        if N_timesteps[-1][i] > timesteps:
            cut_table(i)
            convergence.append(False)
            return
    convergence.append(False)


def cut_table(row):
    N_updates[-1] = N_updates[-1][0:row+1]
    N_timesteps[-1] = N_timesteps[-1][0:row+1]
    Reward_mean[-1] = Reward_mean[-1][0:row+1]
    Reward_median[-1] = Reward_median[-1][0:row+1]
    Reward_min[-1] = Reward_min[-1][0:row+1]
    Reward_max[-1] = Reward_max[-1][0:row+1]
    Reward_std[-1] = Reward_std[-1][0:row+1]
    Entropy[-1] = Entropy[-1][0:row+1]
    Value_loss[-1] = Value_loss[-1][0:row+1]
    Action_loss[-1] = Action_loss[-1][0:row+1]
    N_violation_avg[-1] = N_violation_avg[-1][0:row+1]
    N_goals_avg[-1] = N_goals_avg[-1][0:row+1]
    N_died_avg[-1] = N_died_avg[-1][0:row+1]
    N_end_avg[-1] = N_end_avg[-1][0:row+1]
    N_step_goal_avg[-1] = N_step_goal_avg[-1][0:row+1]


def converged(log_n_steps_goal_avg_curr, log_n_steps_goal_avg_prev, value_lss_curr, mean_rwd_curr, final_rewards_std, log_n_goals_avg_curr):
    return (abs(log_n_steps_goal_avg_curr - log_n_steps_goal_avg_prev) < 0.1
            and value_lss_curr < 0.01
            and mean_rwd_curr > 0.0
            and log_n_goals_avg_curr > 0.0
            )


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

    x_size = 40
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
        plt.fill_between(x, area_bot, area_top, color="skyblue", alpha=0.8)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    return figure


def multi_line_plot(xs, ys, x_label, y_labels, colors, ys_sem=0, title=""):
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
        plt.plot(xs[k], ys[k], colors[k], label=y_labels[k], linewidth=0.3)
        if ys_sem != 0:
            area_top = [ys[k][0]]
            area_bot = [ys[k][0]]
            for l in range(1, len(ys[k])):
                area_bot.append(ys[k][l] - ys_sem[k][l - 1])
                area_top.append(ys[k][l] + ys_sem[k][l - 1])
            plt.fill_between(xs[k], area_bot, area_top, color=colors[k], alpha=0.2)
    plt.legend()
    plt.xlabel('Number of updates (k)')

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


def get_labels():
    env_yes = 0
    env_no = 0
    labels = []
    colors = []
    for i in range(len(envelope)):
        if envelope[i] == 'True':
            labels += ['WiseML' + str(env_yes)]
            colors += ['r']
            env_yes += 1
        else:
            labels += ['SimpleRL' + str(env_no)]
            colors += ['b']
            env_no += 1

    return labels, colors


def avg(iterable):
    if len(iterable) == 0:
        return 0
    return sum(iterable) / len(iterable)


def get_environments(csv_folder_abs_path, criteria):
    environments = set()
    for file_name in os.listdir(csv_folder_abs_path):
        if "a2c" in file_name and ".csv" in file_name and respects_criteria(file_name, criteria):
            environments.add(file_name.split('_')[0])
    return environments


def format_list(a):
    return ' & '.join(list(map(lambda x: "{:10.2f}".format(x), a))).replace('.00', '')


def plot_all(criteria):
    current_directory = os.path.abspath(os.path.dirname(__file__))
    environments = get_environments(current_directory, criteria)
    results = {}
    for env in environments:
        local_criteria = criteria[:]
        local_criteria += [env]
        size = int(env.split('-')[1].replace('s', ''))
        res_yes = plot(local_criteria + ['YES'])
        res_no = plot(local_criteria + ['NO'])
        if size not in results:
            results[size] = {}
        results[size][env] = (res_yes, res_no)

    print("Table 1")
    print(
        'Environment, Envelope, Iteration ,Converged, Min Steps, Avg Steps, Max Steps, Min Mean Rwd, Avg Mean Rwd, Max Min Rwd, Min Goal Steps, Avg Goal Steps, Max Goal Steps \\\\'.replace(
            ',', ' & '))
    for size in sorted(results):
        size_results = results[size]
        for env in size_results:
            # It must be the same number of iterations.
            if len(size_results[env][0]) > 0 and len(size_results[env][1]) > 0 and size_results[env][0][0] == size_results[env][1][0]:
                print(env[10:] + ' & YES & ' + format_list(size_results[env][0][0:]) + '\\\\')
                print(env[10:] + ' &  NO & ' + format_list(size_results[env][1][0:]) + '\\\\')


    print("Table 2")
    for size in sorted(results):
        size_results = results[size]
        avg_steps = 0.0
        compared = 0
        total = 0
        death_nop = 0
        death_sip = 0
        converged_sip = 0
        converged_nop = 0
        for env in size_results:
            #There is at least one iteration of both yes and no.
            if len(size_results[env][0]) > 0 and len(size_results[env][1]) > 0 and \
                size_results[env][0][0] == iterations_number and size_results[env][1][0] == iterations_number:
                if len(size_results[env][0]) > 3 and len(size_results[env][1]) > 3:
                    avg_steps += (1 - (size_results[env][0][3] / size_results[env][1][3]))
                    death_nop += size_results[env][1][-2]
                    death_sip += size_results[env][0][-2]
                    compared += 1
                converged_sip += size_results[env][0][1]
                converged_nop += size_results[env][1][1]
                total += 1

        print(' & '.join("{:10.2f}".format(x) if type(x) == type(float) else str(x) for x in
                         [size, total , avg_steps / compared * 100 if compared > 0 else 'N/A',
                          converged_sip / total if total > 0 else 'N/A', converged_nop / total if total > 0 else 'N/A',
                          death_sip, death_nop]), '\\\\\\hline')



def plot(criteria):
    current_directory = os.path.abspath(os.path.dirname(__file__))

    extract_all_data_from_csv(current_directory, criteria)

    labels, colors = get_labels()

    if len(labels) == 0:
        return []

    values = [[N_timesteps[i][-1] for i in range(len(labels)) if convergence[i]]]
    values += [[Reward_mean[i][-1] for i in range(len(labels)) if convergence[i]]]
    values += [[N_step_goal_avg[i][-1] for i in range(len(labels)) if convergence[i]]]
    values += [[sum(N_died_avg[i][0:-1]) for i in range(len(labels)) if convergence[i]]]

    results = [len(labels), len(values[0]) / len(labels) * 100]
    if len(values[0]) > 0:
        functions = [min, avg, max]
        results += [f(value) for value in values for f in functions]
    return results

'''
    figure_1 = multi_line_plot([N_timesteps[i][:] for i in range(len(labels))],
                               [Reward_mean[i][:] for i in range(len(labels))],
                               "N_updates",
                               labels,
                               colors,
                               [Reward_std[i][:] for i in range(len(labels))])

    Name = "COMPARISON_a2c_" + '_'.join(criteria) + ".pdf"
    print("PdfName : ", Name)

    pdf = PdfPages(current_directory + "/" + Name)

    #pdf.savefig(figure_1)

    pdf.close()
'''

if __name__ == "__main__":
    criteria = []
    for i in range(1, len(sys.argv)):
        criteria += [sys.argv[i]]
    plot_all(criteria)
