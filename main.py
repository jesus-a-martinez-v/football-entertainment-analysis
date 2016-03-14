from combine_files import *
from update_models import *
from plot_data import *
from analysis import *
import pandas as pd
import sys

if __name__ == '__main__':
    args = sys.argv
    store_results = False
    file = None

    if len(args) > 2:
        print "ERROR: Too many arguments."
        sys.exit(-1)
    elif len(args) == 2:
        store_results = True
        file = args[1]

    # First, we must combine the data of each file
    combine_football_data()

    # Then, we'll build our samples them
    mf_names = ['1993-2014-england', '1993-2014-spain', '1993-2014-france', '1993-2014-italy']
    samples_names = ['England', 'Spain', 'France', 'Italy']

    samples = []
    # We will load each sample in a dataframe and calculate the total goals scored in a match, as well as the goal
    # difference for the same match.
    for f in mf_names:
        df = pd.read_csv(f + ".csv")
        df['TG'] = df['FT'].map(total_goals_scored)  # Total goals.
        df['GD'] = df['FT'].map(goal_difference)  # Goal difference.

        samples.append(df)

    samples_min_length = min([len(s) for s in samples])  # We find the minimum length among all samples.
    samples = [s.head(samples_min_length) for s in samples]  # We truncate all samples.
    samples = [{'title': pair[0], 'df': pair[1]} for pair in zip(samples_names, samples)]

    # Now we'll plot some histograms.
    for i in range(len(samples)):
        plot_histogram(samples[i]['df'], mf_names[i] + ".png")

    # Finally, run a proper analysis.
    statistics = descriptive_statistics(samples)
    anova_table, tukey_hsd_table = analysis(samples)

    # Print the results
    if store_results:
        with open(file, 'w') as f:
            f.write(statistics)
            f.write(anova_table)
            f.write(tukey_hsd_table)
    else:
        print statistics
        print anova_table
        print tukey_hsd_table



