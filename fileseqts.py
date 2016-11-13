"""fileseqts.py

A library of functions helpful for investigating and manipulating
sequences of images. Assumes the format "../directory/filename.####.ext"
or "../directory/filename####.ext" with any number of leading zeroes.
"""

import os
import shutil
import re


def gap_check(first_item, last_num):
    """Given the file path of the first file in a sequence and how far 
    out the sequence is supposed to extend, returns a list of the numbers
    of the missing frames. Assumes sequences are in the form xxx####.ext
    or xxx.####.ext"""
    direct, name, numdigits, firstnum, extension = parse_item(first_item)
    
    missing_items = []
    for i in range(firstnum, last_num):
        f = os.path.join(direct, name + add_leading_zeroes(i, numdigits) + extension)
        if not os.path.isfile(f):
            missing_items.append(i)
    return missing_items


def sequence_length(first_item):
    """Given the first file path in a sequence, returns the index of the last sequential file."""
    direct, name, numdigits, firstnum, extension = parse_item(first_item)
    i = firstnum
    nextfile = os.path.join(direct, name + add_leading_zeroes(i, numdigits) + extension)
    while os.path.exists(nextfile):
        i += 1
        nextfile = os.path.join(direct, name + add_leading_zeroes(i, numdigits) + extension)
    return i - 1


def add_leading_zeroes(num, numdigits):
    """Returns a stringified num with zeros prepended until it is at least numdigits digits long."""
    return str(num).zfill(numdigits)


def parse_item(item):
    """Given an item in an image sequence, parses the directory,
    the name, the number of digits, the frame number, and the
    extension of the sequence. Assumes sequences are in the
    format xxx####.ext or xxx.####.ext"""
    directory = os.path.dirname(item)
    filename = os.path.basename(item)
    spl = filename.split('.')
    extension = '.' + spl[-1]
    num_re = re.compile(r'(\d)+$')

    name = num_re.split(".".join(spl[:-1]))[0]
    digits = num_re.search(''.join(spl[:-1])).group()
    numdigits = len(digits)
    return directory, name, numdigits, int(digits), extension


def collapse_list(items):
    """Given an ordered list of numbers, returns the ranges of
    present items. For example, given a list [1,2,3,5,6,7,10], it
    would return the string '1-3, 5-7, 10'."""
    result = ""
    previtem = items[0]
    sequence = False
    for i in items:
        if sequence:
            if not i == previtem + 1:
                sequence = False
                result += "-" + str(previtem) + ", " + str(i)
        else:
            if i == previtem + 1:
                sequence = True
            else:
                result += ", " + str(i)
        previtem = i
    if sequence:
        result += "-" + str(previtem)
    result = result[2:]
    return result


def offset_seq(firstitem, offset, newnumdigits=None):
    """Given the file path to the first item in a complete sequence,
    renumbers each file in the sequence by offseting it by offset.
    THIS WILL OVERWRITE ANY EXISTING FILES."""
    direc, name, numdigits, firstnum, extension = parse_item(firstitem)
    if newnumdigits is None:
        newnumdigits = numdigits
    lastnum = sequence_length(firstitem)
    if offset < 0:
        r = range(firstnum, lastnum + 1, 1)
    else:
        r = range(lastnum, firstnum - 1, -1)

    for i in r:
        src = os.path.join(direc, name + add_leading_zeroes(i, numdigits) + extension)
        dst = os.path.join(direc, name + add_leading_zeroes(i + offset, newnumdigits) + extension)
        shutil.move(src, dst)


def rename_seq(firstitem, newname, newnumdigits=None):
    """Given the file path to the first item in a complete sequence,
    renames each file in the sequence while preserving the files' number.
    THIS WILL OVERWRITE ANY EXISTING FILES."""
    direc, name, numdigits, firstnum, extension = parse_item(firstitem)
    if newnumdigits is None:
        newnumdigits = numdigits
    lastnum = sequence_length(firstitem)

    for i in range(firstnum, lastnum + 1):
        src = os.path.join(direc, name + add_leading_zeroes(i, numdigits) + extension)
        dst = os.path.join(direc, newname + add_leading_zeroes(i, newnumdigits) + extension)
        shutil.move(src, dst)


def reverse_seq(firstitem, writeto=None):
    """Given the file path to the first item in a complete sequence,
    reverses the sequence. writeto is an optional directory to place
    the reversed sequence; if it is not specified, the sequence will be
    reversed in place. THIS WILL OVERWRITE ANY EXISTING FILES."""
    direc, name, numdigits, firstnum, extension = parse_item(firstitem)
    lastnum = sequence_length(firstitem)
    
    if writeto:
        if not os.path.exists(writeto):
            os.mkdir(writeto)
        for i in range(firstnum, lastnum + 1):
            newindex = lastnum + firstnum - i
            src = os.path.join(direc, name + add_leading_zeroes(i, numdigits) + extension)
            dst = os.path.join(writeto, name + add_leading_zeroes(newindex, numdigits) + extension)
            shutil.copyfile(src, dst)
    else:
        for i in range(firstnum, int((lastnum - firstnum) / 2) + firstnum + 1):
            newindex = lastnum + firstnum - i
            if newindex != i:
                src = os.path.join(direc, name + add_leading_zeroes(i, numdigits) + extension)
                dst = os.path.join(direc, name + add_leading_zeroes(newindex, numdigits) + extension)
                shutil.move(dst, dst+"_TEMP")
                shutil.move(src, dst)
                shutil.move(dst+"_TEMP", src)