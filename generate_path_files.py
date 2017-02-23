#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate path files for pypaw

:copyright:
   Ridvan Orsvuran (orsvuran@geoazur.unice.fr), 2017
:license:
    GNU Lesser General Public License, version 3 (LGPLv3)
    (http://www.gnu.org/licenses/lgpl-3.0.en.html)
"""

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import argparse
import os
import json
import yaml


def load_yaml(filename):
    with open(filename) as f:
        data = yaml.load(f)
    return data


def load_events(filename):
    with open(filename) as f:
        events = [line.replace("\n", "") for line in f]
    return events


def parse_folder(folder, parent):
    name, data = folder.items()[0]
    paths = {}
    files = {}
    if isinstance(data, str):
        path = data
        subfolders = []
        child_files = []
    else:
        path = data.get("path", name)
        subfolders = data.get("subfolders", [])
        child_files = data.get("files", [])

    paths[name] = os.path.join(parent, path)

    for child_file in child_files:
        fname, filepath = child_file.items()[0]
        files[fname] = os.path.join(paths[name], filepath)

    for subfolder in subfolders:
        sub_paths, sub_files = parse_folder(subfolder,
                                            paths[name])
        paths.update(sub_paths)
        files.update(sub_files)

    return paths, files


def load_path_config(filename):
    data = load_yaml(filename)
    root = os.getcwd()
    folders = {}
    files = {}
    for subfolder in data:
        subfolders, subfiles = parse_folder(subfolder,
                                            parent=root)
        folders.update(subfolders)
        files.update(subfiles)
    return folders, files


def makedir(dirname):
    try:
        os.makedirs(dirname)
    except:
        pass


def dump_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    print("{} is written.".format(filename))


def f(name, eventname=None, period_band=None):
    return files[name].format(eventname=eventname,
                              period_band=period_band)


def d(name, eventname=None, period_band=None):
    return folders[name].format(eventname=eventname,
                                period_band=period_band)


def generate_folders():
    for eventname in events:
        for name, path in folders.iteritems():
            makedir(path.format(eventname=eventname))


def generate_converter():
    for eventname in events:
        for seis_type in ["obsd", "synt"]:
            data = {
                "filetype": "sac",
                "output_file": f("raw_"+seis_type, eventname),
                "tag": settings["raw_{}_tag".format(seis_type)],
                "quakeml_file": f("quakeml", eventname),
                "staxml_dir": d("staxml", eventname),
                "waveform_dir": d("{}_sac".format(seis_type), eventname)
            }
            dump_json(data,
                      f("{}_converter_path".format(seis_type), eventname))


if __name__ == '__main__':
    folders, files = load_path_config("paths.yml")
    settings = load_yaml("settings.yml")
    events = load_events("event_list")
    steps = dict([(x[9:], x) for x in locals().keys()
                  if x.startswith('generate_')])
    parser = argparse.ArgumentParser(
        description='Generate path files')
    parser.add_argument("step",  help="file to generate",
                        choices=steps.keys())
    args = parser.parse_args()
    locals()[steps[args.step]]()
