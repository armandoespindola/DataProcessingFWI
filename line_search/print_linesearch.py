#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals
import sys
import os
sys.path.append('../')

import argparse
from generate_path_files import FileOperator
from tqdm import tqdm
from pprint import pprint

MISFIT_SINGLE = 1
MISFIT_DD = 2
MISFIT_BOTH = 3

FileIO = FileOperator()

# load_json = FileOperator.load_json
# load_yaml = FileOperator.load_yaml
# load_events = FileOperator.load_events


def read_weights_rec(event, period_band):
    return FileIO.load_json(
        "./weights/output/{}/window_weights.{}.json".format(
            event, period_band
        )
    )


def read_weights_paired(event, period_band):
    return FileIO.load_json(
        "./weights/output/{}/category/window_weights.paired.{}.json".format(
            event, period_band
        )
    )


def it_meas(data):
    """Generator for ease of reading..."""
    for sta, sta_meas in data.items():
        for comp, comp_meas in sta_meas.items():
            yield sta, comp, comp_meas




def read_measurements(name, rec_weights, paired_weights, events, period_bands,
                      use_meas = MISFIT_SINGLE):
    mt_folder = "./measure/output"
    dd_folder = "./measure/dd_output"
    if name != ".":
        mt_folder += "_"+name
        dd_folder += "_"+name

    misfit = {p: {c: 0.0 for c in "RTZ"}
              for p in period_bands}


    for e in events:
        for p in period_bands:

            if use_meas & MISFIT_SINGLE:
                data = FileIO.load_json(mt_folder+"/measure.{}.{}.json.filter".format(e, p))
                for _, comp, comp_meas in it_meas(data):
                    c = comp[-1]
                    w = 0.0
                    try:
                        w = rec_weights[e, p][comp]["weight"]
                        print("weight ",p,comp," :", w)
                    except KeyError as err:
                        if not comp in str(err):
                            raise err
                        w = 0.0
                    for m in comp_meas:
                        misfit[p][c] += m["misfit_dt"]

            # if use_meas & MISFIT_DD:
            #     data = FileIO.load_json(dd_folder+"/dd_measure.{}.{}.json".format(e, p))
            #     for c, pair_meas in data.items():
            #         for meas_name, dd_meas in pair_meas.items():
            #             comp = meas_name.split(":")[0]
            #             try:
            #                 w = paired_weights[e, p][comp]["weight"]
            #             except KeyError as err:
            #                 if not comp in str(err):
            #                     raise err
            #                 w = 0.0

            #             for m in dd_meas:
            #                 misfit[p][c] += w*m["misfit"]

    return misfit

if __name__ == "__main__":
    os.chdir('../')
    parser = argparse.ArgumentParser(description="Print misfits")
    parser.add_argument("misfits", nargs="+", help="misfits")
    args = parser.parse_args()

    events = FileIO.load_events(filename="event_list")
    period_bands = FileIO.load_yaml("settings.yml")["period_bands"]
    ncat = len(events)*len(period_bands)
    pbar = tqdm(total=ncat, desc="Weights")
    rec_weights = {}
    paired_weights = {}
    for e in events:
        for p in period_bands:
            rec_weights[e, p] = read_weights_rec(e, p)
            #paired_weights[e, p] = read_weights_paired(e, p)
            pbar.update()

    misfits = []
    for name in tqdm(args.misfits, "Measurements"):
        misfits.append(read_measurements(name, rec_weights, paired_weights,
                                         events, period_bands,
                                         use_meas = MISFIT_SINGLE))


    total_misfits = []
    for m in misfits:
        total_misfit = 0.0
        for p in period_bands:
            for c in "RTZ":
                print(p,c,m[p][c])
                total_misfit += m[p][c]
        total_misfits.append(total_misfit)

    print("\n\n")
    pprint(misfits)
    print("Total Misfits:", total_misfits[0])

    f=open("fval",'w')
    f.write("%f" % (total_misfits[0]))
    f.close()
