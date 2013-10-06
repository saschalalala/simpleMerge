#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""@package Merge
Merges two files and keeps the commented lines

If you update your proxy blacklist, all commented lines you entered to whitelist several URLs are overwritten.
"""


__author__ = 'Sascha'

import argparse  # To parse arguments from command line
import shutil    # To copy files
import os.path   # To check if a file exists
import locale    # To sort in the same way as the linux sort command

locale.setlocale(locale.LC_ALL, "")


def read_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        lines1 = f1.read().splitlines()
        lines2 = f2.read().splitlines()
    f1.close()
    f2.close()
    merged = lines1 + lines2
    return sorted(list(set(merged)), key=locale.strxfrm)


def backup(file):
    backupfile = "." + file + ".bak"
    shutil.copy2(file, backupfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="The first file.")
    parser.add_argument("file2", help="The second file.")
    parser.add_argument("output", help="The output file. If output exists, it is copied to .output.bak")
    args = parser.parse_args()
    file1 = args.file1
    file2 = args.file2
    output = args.output
    if os.path.isfile(output):
        backup(output)
    merged_list = read_files(file1, file2)
    i = 0
    while i < len(merged_list) - 1:
        if merged_list[i] == merged_list[i+1][1:]:  # if readed line is the same as nextline-firstchar (Which is the comment char, anything else is bullshit)
            del merged_list[i]
            i -= 1  # the list is shrinked, when elements are deleted
        i += 1

    # write the output to the output file
    of = open(output, 'w+')
    of.truncate()  # delete all contents
    of.write("\n".join(merged_list))
    of.close()


if __name__ == "__main__":
    main()
