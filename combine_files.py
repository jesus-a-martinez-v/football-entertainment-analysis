import os


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
