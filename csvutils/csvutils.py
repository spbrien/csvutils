# -*- coding: utf-8 -*-

"""Main module."""

import csv
import collections


# Utilities
# -------------------
# to centralize text input handling
# encode str as unicode, ignore errors
def u_ignore(str):
    return unicode(str, 'utf-8', 'ignore')


# decode unicode to ascii, ignore errors (strip special characters)
def u_strip(u_str):
    return u_str.encode('utf-8', 'ignore').decode('ascii', 'ignore')


def uniq(oldlist):
    cleanlist = []
    for x in oldlist:
        if x not in cleanlist:
            cleanlist.append(x)
    return cleanlist


def uniq_objs(items, attrs):
    def get_attrs_from_list(item, attrs):
        for attr in attrs:
            yield item[attr]

    obj_list = [
        tuple(
            [i for i in get_attrs_from_list(item, attrs)]
        ) for item in items
    ]
    non_unique_indexes = [
        idx for idx, item
        in enumerate(collections.Counter(obj_list).items())
        if item[1] > 1
    ]
    for item in non_unique_indexes:
        items.pop(item)

    return items


# Getting Data
# -------------------
def get_tsv_data(f):
    with open(f,'rU') as tsvin:
        tsvin = csv.reader(tsvin, dialect=csv.excel_tab)
        return [
            [
                u_ignore(cell) for cell in row
            ] for row in tsvin if any(row)
        ]


def get_tsv_dict(f):
    with open(f,'rU') as tsvin:
        tsvin = csv.DictReader(tsvin, dialect=csv.excel_tab)
        return [
            {
                u_ignore(key): u_ignore(value)
                for key, value in row.iteritems()
            } for row in tsvin if any(row)
        ]


def write_row_splits(splits):
    for k, v in splits.iteritems():
        with open("%s.tsv" % k, 'w') as out:
            w = csv.writer(out)
            for i in v:
                w.writerow(v)


def create_row_splits(l):
    def process_items(items):
        return ({
            name: predicate(item)
            for name, predicate in l
        } for item in items)
    return process_items


def split_tsv_by_row(f, condition_list=None):
    def process(condition_list):
        split_factory = create_row_splits(condition_list)
        with open(f,'rU') as tsvin:
            tsvin = csv.reader(tsvin, dialect=csv.excel_tab)
            splits = split_factory(tsvin)
        write_row_splits(splits)

    return process(condition_list) if condition_list else process
