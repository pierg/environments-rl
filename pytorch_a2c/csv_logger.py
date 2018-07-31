import csv
import os

current_csv_file = ""

def create_header(csv_file, headers):
    """
    Creates headers in a csv file
    :param csv_file: A csv file to write to
    :param headers: a list containing the headers wanted, e.g ['Date', 'Tempratrue 1', ... ]
    :return: void
    """
    global current_csv_file
    current_csv_file = csv_file

    with open(csv_file, 'w+', newline='') as csv_log:
        writer = csv.writer(csv_log, delimiter=',')
        writer.writerow(headers)

def write_to_log(values):
    """
    Writes a row to a csv log file, appends to an existing file
    :param values: A list of values that will be written in the CSV files, ensure they follow the same order
    as the headers in the CSV file
    :return: void
    """
    with open(current_csv_file, 'a', newline='') as csv_log:
        writer = csv.writer(csv_log, delimiter=',')
        writer.writerow(values)
