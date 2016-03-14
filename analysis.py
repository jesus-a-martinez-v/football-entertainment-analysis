import os
import math
import pandas as pd
import numpy as np
import scipy.stats as stats


def descriptive_statistics(info):
    for i in info:
        print i['title']
        print i['df'].describe()
        print '____________________'


def anova_table(dfs):
    samples = []
    for df in dfs:
        samples.append(df['TG'])

    q = 3.65
    k = len(samples)
    n = len(samples[0])
    degrees_between = k - 1
    degrees_within = k * (n - 1)
    samples_means = [np.mean(sample) for sample in samples]
    grand_mean = np.mean(samples_means)
    ss_between = n * sum([(s - grand_mean) ** 2 for s in samples_means])
    ss_within = 0

    for i in range(k):
        ss_within += sum([(x - samples_means[i]) ** 2 for x in samples[i]])

    ms_between = ss_between / degrees_between
    ms_within = ss_within / degrees_within
    f_statistic = ms_between / ms_within
    hsd = q * math.sqrt(ms_within/n)

    table = """
        ----------------------------------------------------------------------------
        | SS Between: %.3f
        | df between: %d
        | SS Within:  %.3f
        | df within: %d
        | MS Between: %.3f
        | MS Within: %.3f
        |
        | F-statistic: %.3f
        ----------------------------------------------------------------------------
        """ % (float(ss_between), degrees_between, float(ss_within), degrees_within, float(ms_between),
               float(ms_within), float(f_statistic))

    print table
    _, p = stats.f_oneway(samples[0], samples[1], samples[2], samples[3])
    print "p = " + str(p)
    print "Tukey's HSD: " + str(hsd)

    print "ENGLAND - SPAIN"
    print "|" + str(samples_means[0]) + " - " + str(samples_means[1]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[0] - samples_means[1]) > hsd)
    print "ENGLAND - FRANCE"
    print "|" + str(samples_means[0]) + " - " + str(samples_means[2]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[0] - samples_means[2]) > hsd)
    print "ENGLAND - ITALY"
    print "|" + str(samples_means[0]) + " - " + str(samples_means[3]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[0] - samples_means[3]) > hsd)
    print "SPAIN - FRANCE"
    print "|" + str(samples_means[1]) + " - " + str(samples_means[2]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[1] - samples_means[2]) > hsd)
    print "SPAIN - ITALY"
    print "|" + str(samples_means[1]) + " - " + str(samples_means[3]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[1] - samples_means[3]) > hsd)
    print "FRANCE - ITALY"
    print "|" + str(samples_means[2]) + " - " + str(samples_means[3]) + "| > " + str(hsd) + " ===> " + str(abs(samples_means[2] - samples_means[3]) > hsd)

    print '--------'
    print 'Explained variation:'
    print str(ss_between / (ss_between + ss_within))

if __name__ == '__main__':
    mf_names = ['1993-2014-england', '1993-2014-spain', '1993-2014-france', '1993-2014-italy']
    dataframes = []

    for f in mf_names:
        df = pd.read_csv("updated_" + f + ".csv")
        dataframes.append(df.head(7166))
        # df['TG_normalized'] = np.log1p(df['TG'])
        # plot_histograms(df.head(7166), f + ".png")

    descriptive_statistics([{'title': pair[0], 'df': pair[1]['TG']} for pair in zip(['England', 'Spain', 'France', 'Italy'], dataframes)])
    anova_table(dataframes)
