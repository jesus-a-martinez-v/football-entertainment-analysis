import pandas as pd
import matplotlib.pylab as P
import scipy.stats as s
from ggplot import *
import numpy as np


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
        print f
        print dataframe['TG'].describe()  # TODO This must be done somewhere else...
        print '--------------------------------------------------'
        # dataframe['TG_log'] = np.log1p(dataframe['TG']).hist()
        # samples.append(dataframe['TG'].head(7166))
        # samples_log1p.append(np.log1p(dataframe['TG'].head(7166)))
        # print(np.log1p(dataframe['TG'].head(7166)).describe())

        # plot = ggplot(aes(x='TG'), data=dataframe.head(7166)) + geom_histogram(binwidth=1)
        # ggsave(f + ".png", plot)
        dataframe.to_csv('updated_' + f)

        # print(s.f_oneway(samples_log1p[0], samples_log1p[1], samples_log1p[2], samples_log1p[3]))
