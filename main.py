import os
from ggplot import *
import pandas as pd
import numpy as np


def combine_football_data():
    """
    For each of our for datasets, it combines the data that spans between the season 1993-94 until 2013-14 in one single
    file per football league. The merging file will be called 1993-2014-xxxx, where xxxx stands for 'england', 'spain',
    'italy' or 'france'.
    """
    for directory in os.listdir("./data"):
        master_file_name = "1993-2014-" + str(directory) + ".csv"  # We'll have one master file per data set.
        with open(master_file_name, 'w') as master_file:
            master_file.write("Date,Team 1,Team 2,FT,HT\n")  # We write the CSV header once.

            # For each file, we will write all of its data in the master file defined above.
            for filename in os.listdir("./data/" + directory):
                with open("./data/" + directory + "/" + filename, 'r') as f:
                    header_line = True  # Flag used to ignore the CSV header of each file.
                    for line in f:
                        if header_line:
                            header_line = False
                            continue

                        master_file.write(line)


def total_goals_scored(ft):
    """
    Takes the final time score and adds each component to obtain the total goals scored in the match.
    """
    goals = ft.split("-")
    return int(goals[0]) + int(goals[1])


def goal_difference(ft):
    """
    Takes the final time score and obtains the goal difference of the match.
    """
    goals = ft.split("-")
    return abs(int(goals[0]) - int(goals[1]))


if __name__ == "__main__":
    master_files = ['1993-2014-england.csv', '1993-2014-spain.csv', '1993-2014-france.csv', '1993-2014-italy.csv']
    samples = []
    samples_log1p = []
    for f in master_files:
        dataframe = pd.read_csv(f)
        dataframe['TG'] = dataframe['FT'].map(total_goals_scored)  # Total goals.
        dataframe['GD'] = dataframe['FT'].map(goal_difference)  # Goal difference.

        # dataframe['TG_log'] = np.log1p(dataframe['TG']).hist()
        # samples.append(dataframe['TG'].head(7166))
        # samples_log1p.append(np.log1p(dataframe['TG'].head(7166)))
        # print(np.log1p(dataframe['TG'].head(7166)).describe())

        # plot = ggplot(aes(x='TG'), data=dataframe.head(7166)) + geom_histogram(binwidth=1)
        # ggsave(f + ".png", plot)
        dataframe.to_csv('updated_' + f)

        # print(s.f_oneway(samples_log1p[0], samples_log1p[1], samples_log1p[2], samples_log1p[3]))


def plot_histograms(df, filename):
    """

    """
    raw_plot = ggplot(aes(x='TG'), data=df) + geom_histogram(binwidth=1)  # Histogram for raw data.
    ggsave(raw_plot, filename)  # Save it.

    # Histogram for normalized data.
    normalized_plot = ggplot(aes(x='TG_normalized'), data=df) + geom_histogram(binwidth=0.4)
    ggsave(normalized_plot, "normalized_" + filename)  # Save it.


if __name__ == '__main__':
    mf_names = ['1993-2014-england', '1993-2014-spain', '1993-2014-france', '1993-2014-italy']

    for f in mf_names:
        df = pd.read_csv("updated_" + f + ".csv")
        df['TG_normalized'] = np.log1p(df['TG'])
        plot_histograms(df.head(7166), f + ".png")
