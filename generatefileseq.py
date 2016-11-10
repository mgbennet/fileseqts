"""generatefileseq.py

A small library of functions for generating file sequences. Useful
for testing imgseqlib.py.
"""

import os
import random


def make_seq(directory, filename, num_files, num_digits=0, first_num=1):
    """Creates a file sequence in 'directory'. Has digit padding of 'num_digits'."""
    return make_seq_withholes(directory, filename, num_files,
                                miss_ratio=-1, num_digits=num_digits, first_num=first_num)[0]


def make_seq_withholes(directory, filename, num_files, miss_ratio=.2, num_digits=0, first_num=1):
    """Creates an incommplete file sequence in 'directory'. Each file has a 'miss_ratio' chance of
    being skipped, where 'miss_ratio' is between 0 and 1. Has digit padding of 'num_digits'."""
    if num_files <= 0:
        raise ValueError("num_files must be a positive integer")
    if not os.path.isdir(directory):
        os.mkdir(directory)
    made = []
    missed = []
    for i in range(first_num, num_files + 1):
        if random.random() >= miss_ratio:
            file_path = "{0}.{1}.txt".format(filename, str(i).zfill(num_digits))
            file_path = os.path.join(directory, file_path)
            with open(file_path, "w") as f:
                f.write(str(i))
                made.append(f.name)
        else:
            missed.append(i)
    return made, missed


def make_seq_primeholes(directory, filename, num_files, num_digits=0):
    """Creates an incomplete file sequence in 'directory'. Any file that would have a prime number
    is skipped. Has digit padding of 'num_digits'."""
    if num_files <= 0:
        raise ValueError("num_files must be a positive integer")
    if not os.path.isdir(directory):
        os.mkdir(directory)
    made = []
    missed = []
    erat_sieve = [True] * num_files
    for i in range(1, num_files + 1):
        if erat_sieve[i - 1] and i > 1:
            for j in range(i*i, num_files + 1, i):
                erat_sieve[j - 1] = False
            missed.append(i)
        else:
            file_path = "{0}.{1}.txt".format(filename, str(i).zfill(num_digits))
            file_path = os.path.join(directory, file_path)
            with open(file_path, "w") as f:
                f.write(str(i))
                made.append(f.name)
    return made, missed