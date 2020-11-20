from argparse import ArgumentParser
import os.path
import numpy as np
import csv

NUM_CONDITIONS = 27
NUM_BLOCKS = 3

DV_TIME = 5
DV_MISSES = 6

CURSOR_MAP = {
    "BUBBLE": 0,
    "AREA": 1,
    "POINT": 2
}

BG_MAP = {
    "WHITE": 0,
    "YELLOW": 1,
    "BLACK": 2
}

TARGET_MAP = {
    "20": 0,
    "40": 1,
    "80": 2
}


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The directory does not exist." % arg)
    return arg


def get_condition_no(cursor, background_colour, target_count):
    return TARGET_MAP[target_count] + BG_MAP[background_colour]*3 + CURSOR_MAP[cursor]*9


def generate_anova(participant_data):
    time_matrix = np.zeros(NUM_CONDITIONS, dtype=float)
    error_rate_matrix = np.zeros(NUM_CONDITIONS, dtype=float)

    with open(participant_data) as f:
        raw_data = f.read().splitlines()
        header = raw_data[0]

        # Remove block seperators
        data = "\n".join(raw_data[1:]).split('------')
        # Remove final block line
        data.pop()
        if len(data) != NUM_BLOCKS * NUM_CONDITIONS:
            print('Improper data length.')
            exit(1)

        # Generate blocks
        for i in range(0, len(data), 3):
            # Read CSV for block
            block = [sub_block.strip() for sub_block in data[i:i+3]]
            block_lines = "\n".join(block).splitlines()
            reader = csv.reader(block_lines, delimiter='\t')
            csv_lines = list(reader)

            # Get IV for block
            cursor, background_colour, target_count = csv_lines[0][2], csv_lines[0][3], csv_lines[0][4]
            condition = get_condition_no(cursor, background_colour, target_count)

            # Get the DV values
            times = np.array([float(line[DV_TIME]) for line in csv_lines], dtype=float)
            error_rate = np.array([float(line[DV_MISSES]) / (float(line[DV_MISSES]) + 1) for line in csv_lines], dtype=float)

            # Add the DV mean to their respective condition number
            time_matrix[condition] = times.mean()
            error_rate_matrix[condition] = error_rate.mean()

        return time_matrix, error_rate_matrix


if __name__ == '__main__':

    parser = ArgumentParser(description="ikjMatrix multiplication")
    parser.add_argument("-d", dest="data_dir", required=True,
                        help="input file", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    data_dir = args.data_dir

    participant_data_fps = []

    # Get all participant data files
    for file in os.listdir(data_dir):
        full_path = os.path.join(data_dir, file)
        if os.path.isfile(full_path) and full_path.endswith('.txt'):
            participant_data_fps.append(full_path)

    anova_time_matrix = np.zeros((len(participant_data_fps), NUM_CONDITIONS), dtype=float)
    anova_error_rate_matrix = np.zeros((len(participant_data_fps), NUM_CONDITIONS), dtype=float)

    for i,fp in enumerate(sorted(participant_data_fps)):
        participant_time_matrix, participant_error_rate_matrix = generate_anova(fp)
        # Add the participant rows
        anova_time_matrix[i] = participant_time_matrix
        anova_error_rate_matrix[i] = participant_error_rate_matrix

    # Write the files as CSV
    np.savetxt("anova_time.txt", anova_time_matrix, delimiter=",")
    np.savetxt("anova_error_rate.txt", anova_time_matrix, delimiter=",")

