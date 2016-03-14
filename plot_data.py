from ggplot import *
import pandas as pd
import numpy as np


def plot_histograms(df, filename):
    """

    """
    raw_plot = ggplot(aes(x='TG'), data=df) + geom_histogram(binwidth=1) + ggtitle("Goals scored by match") + xlab('Goals') + ylab('Frequency') # Histogram for raw data.
    ggsave(raw_plot, filename)  # Save it.


if __name__ == '__main__':
    mf_names = ['1993-2014-england', '1993-2014-spain', '1993-2014-france', '1993-2014-italy']

    for f in mf_names:
        df = pd.read_csv("updated_" + f + ".csv")
        plot_histograms(df.head(7166), f + ".png")
