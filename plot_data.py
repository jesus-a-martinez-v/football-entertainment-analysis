from ggplot import *


def plot_histogram(df, filename, title="Goals scored by match", x_label='Goals', y_label='Frequency'):
    """
    Plots a histogram of the given dataframe, and stores it in the file indicated in filename.
    """
    raw_plot = ggplot(aes(x='TG'), data=df) + geom_histogram(binwidth=1) + ggtitle(title) + xlab(x_label) + \
               ylab(y_label)  # Histogram for raw data.
    ggsave(raw_plot, filename)  # Save it.
