import math
import numpy as np
import scipy.stats as stats


def descriptive_statistics(samples):
    """
    Builds a table of descriptive statistics for the samples.
    """
    table = ""
    for sample in samples:
        table += "%s\n----------\n%s\n__________________________________\n\n" % (
            sample['title'], sample['df']['TG'].describe())

    return table


def analysis(samples):
    """
    Perform an ANOVA and Tukey's HSD tests on the samples.
    It returns the corresponding ANOVA and Pairwise Tukey tables.
    """
    samples_data = []
    for sample in samples:
        samples_data.append(sample['df']['TG'])

    k = len(samples_data)  # Number of groups.
    n = len(samples_data[0])  # Length of each groups.
    degrees_between = k - 1  # Degrees of freedom between groups.
    degrees_within = k * (n - 1)  # Degrees of freedom within groups.
    samples_means = [np.mean(sample) for sample in samples_data]  # Mean of each sample group.
    grand_mean = np.mean(samples_means)  # Grand mean (in this case, the mean of means).
    ss_between = n * sum([(s - grand_mean) ** 2 for s in samples_means])  # Sum of squares between groups.
    ss_within = 0  # Sum of squares within groups.

    for i in range(k):
        ss_within += sum([(x - samples_means[i]) ** 2 for x in samples_data[i]])

    ms_between = ss_between / degrees_between
    ms_within = ss_within / degrees_within

    f_statistic = ms_between / ms_within
    _, p = stats.f_oneway(samples_data[0], samples_data[1], samples_data[2], samples_data[3])

    q = 3.65  # Q-statistic.
    hsd = q * math.sqrt(ms_within / n)  # Tukey's Honestly Significant Difference coefficient.

    anova_table = """
        ----------------------------------------------------------------------------
        | SS Between: %.3f
        | df between: %d
        | SS Within:  %.3f
        | df within: %d
        | MS Between: %.3f
        | MS Within: %.3f
        |
        | F-statistic: %.3f
        | p-value:     %s
        ----------------------------------------------------------------------------
        """ % (float(ss_between), degrees_between, float(ss_within), degrees_within, float(ms_between),
               float(ms_within), float(f_statistic), str(p))

    tukey_hsd_table = tukey_table(list(map(lambda sample: sample['title'], samples)), samples_means, hsd)

    return anova_table, tukey_hsd_table


def tukey_table(samples_names, means, hsd):
    """
    Builds a pairwise Tukey's table. It compares the means of each pair of groups with the HSD coefficient to
    determine if the difference between them is honestly significant.
    """

    k = len(samples_names)

    row_format = "%s\t|\t%s\t|\t%s\n"
    table = "GROUP 1\t|\tGROUP 2\t|\tSignificant difference?\n----------------------------------------------\n"
    for i in range(k):
        for j in range(i + 1, k):
            table += row_format % (samples_names[i], samples_names[j],
                                   'Yes' if abs(means[i] - means[j]) > hsd else 'No')

    return table
