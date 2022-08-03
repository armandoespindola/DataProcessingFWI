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
import subprocess

class FileOperator(object):
    """Documentation for FileOperator

    """
    def __init__(self):
        super(FileOperator, self).__init__()

    def load_json(self, filename):
        with open(filename) as f:
            data = json.load(f)
        return data

    def dump_json(self, data, filename):
        with open(filename, "w") as file_:
            json.dump(data, file_, indent=2, sort_keys=True)
        print("{} is written.".format(filename))

    def load_yaml(self, filename):
        with open(filename) as f:
            data = yaml.safe_load(f)
        return data

    def dump_yaml(self, data, filename):
        with open(filename, "w") as f:
            data = yaml.safe_dump(data, f, indent=2)
        return data
        print("{} is written.".format(filename))

    def load_events(self, filename):
        with open(filename) as f:
            events = [line.replace("\n", "") for line in f if not line.startswith('#')]
        return events
    
    def parse_folder(self, folder, parent):
        name, data = list(folder.items())[0]
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
            fname, filepath = list(child_file.items())[0]
            files[fname] = os.path.join(paths[name], filepath)

        for subfolder in subfolders:
            sub_paths, sub_files = self.parse_folder(subfolder,
                                                     paths[name])
            paths.update(sub_paths)
            files.update(sub_files)

        return paths, files

    def load_path_config(self, filename):
        data = self.load_yaml(filename)
        root = os.getcwd()
        folders = {}
        files = {}
        for subfolder in data:
            subfolders, subfiles = self.parse_folder(subfolder,
                                                     parent=root)
            folders.update(subfolders)
            files.update(subfiles)
        return folders, files

    def makedir(self, dirname):
        try:
            os.makedirs(dirname)
        except OSError:
            pass


class FileGenerator(FileOperator):
    """Documentation for FileGenerator

    """
    def __init__(self):
        super(FileGenerator, self).__init__()
        self.generators = []

    def f(self, name, eventname=None, period_band=None):
        return self.files[name].format(eventname=eventname,
                                       period_band=period_band)

    def d(self, name, eventname=None, period_band=None):
        return self.folders[name].format(eventname=eventname,
                                         period_band=period_band)

    def generate_list_events(self):
        for eventname in self.events:
            print(eventname)

    def generate_list_period_bands(self):
        for period_band in self.settings["period_bands"]:
            print(period_band)

    def generate_folders(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                for name, path in self.folders.items():
                    self.makedir(path.format(eventname=eventname,
                                             period_band=period_band))

    def generate_converter(self):
        for eventname in self.events:
            for seis_type in ["obsd", "synt"]:
                data = {
                    "filetype": "sac",
                    "output_file": self.f("raw_"+seis_type, eventname),
                    "tag": self.settings["raw_{}_tag".format(seis_type)],
                    "quakeml_file": self.f("quakeml", eventname),
                    "staxml_dir": self.d("staxml", eventname),
                    "waveform_dir": self.d("{}_sac".format(seis_type),
                                           eventname)
                }
                self.dump_json(data,
                               self.f("{}_converter_path".format(seis_type),
                                      eventname))

    def generate_proc(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                for seis_type in ["obsd", "synt"]:
                    data = {
                        "input_asdf": self.f("raw_"+seis_type, eventname),
                        "input_tag": self.settings["raw_{}_tag".format(seis_type)],  # NOQA
                        "output_asdf": self.f("proc_"+seis_type,
                                              eventname, period_band),
                        "output_tag": self.settings["proc_{}_tag".format(seis_type)]  # NOQA
                    }
                    self.dump_json(data,
                                   self.f("{}_proc_path".format(seis_type),
                                          eventname, period_band))

    def generate_windows(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("windows_file", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"]
                }
                self.dump_json(data,
                               self.f("window_path", eventname, period_band))

    def generate_measure(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("measure_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("measure_file", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("measure_path", eventname, period_band))

    def generate_stations(self):
        for eventname in self.events:
            data = {
                "input_asdf": self.f("raw_synt", eventname),
                "outputfile": self.f("stations_file", eventname),
            }
            self.dump_json(data,
                           self.f("stations_path", eventname))

    def generate_filter(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "measurement_file": self.f("measure_file", eventname, period_band),  # NOQA
                    "output_file": self.f("windows_filter_file", eventname, period_band),  # NOQA
                    "station_file": self.f("stations_file", eventname),
                    "window_file": self.f("windows_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("filter_path", eventname, period_band))

    def generate_adjoint(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("adjoint_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("adjoint_file", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("adjoint_path", eventname, period_band))
                

    def generate_adjoint_dt(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("adjoint_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("adjoint_file_dt", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("adjoint_path_dt", eventname, period_band))


    def generate_adjoint_am(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("adjoint_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("adjoint_file_am", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("adjoint_path_am", eventname, period_band))

    def generate_adjoint_dt_q(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("adjoint_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("adjoint_file_dt_q", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("adjoint_path_dt_q", eventname, period_band))


    def generate_adjoint_am_q(self):
        for eventname in self.events:
            for period_band in self.settings["period_bands"]:
                data = {
                    "figure_dir": self.d("adjoint_figures"),
                    "figure_mode": False,
                    "obsd_asdf": self.f("proc_obsd", eventname, period_band),
                    "obsd_tag": self.settings["proc_obsd_tag"],
                    "output_file": self.f("adjoint_file_am_q", eventname, period_band),  # NOQA
                    "synt_asdf": self.f("proc_synt", eventname, period_band),
                    "synt_tag": self.settings["proc_synt_tag"],
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
                self.dump_json(data,
                               self.f("adjoint_path_am_q", eventname, period_band))


    def get_dt_and_am_weights(self):
        from tqdm import tqdm
        total_dt_misfit = 0.0
        total_amp_misfit = 0.0
        pbar = tqdm(total=len(self.settings["period_bands"]*len(self.events)),
                    desc="Computing raw total misfits")
        for per_band in self.settings["period_bands"]:
            for eventname in self.events:
                measurements = self.load_json(self.f("measure_file",
                                       eventname, per_band)).items()
                for sta, sta_meas in measurements:
                    for comp, comp_meas in sta_meas.items():
                        for meas in comp_meas:
                            total_dt_misfit += meas["misfit_dt"]
                            total_amp_misfit += meas["misfit_dlna"]
                            pbar.update()

        print(" (DT,AM) Total Misfit : ",total_dt_misfit,total_amp_misfit)
        total_misfit = total_dt_misfit + total_amp_misfit
        weight_tt = total_amp_misfit/total_misfit
        weight_amp = total_dt_misfit/total_misfit
        print(" (DT,AM) Weights Misfit : ",weight_tt,weight_amp)
        return weight_tt, weight_amp



    def generate_misfit_main(self,file_weight,misfit_type):
        from tqdm import tqdm
        # Read Weights
        weight = {}
        
        for e in self.events:
            for p in self.settings['period_bands']:
                weight[e,p] = self.load_json(self.f(file_weight,e,p))

        misfit = {p: {c: 0.0 for c in "RTZ"} for p in self.settings['period_bands']}

        total_misfit = 0.0
        
        pbar = tqdm(total=len(self.settings["period_bands"]*len(self.events)),
                    desc="Computing raw total misfits")
        for per_band in self.settings["period_bands"]:
            for eventname in self.events:
                measurements = self.load_json(self.f("measure_file_filter",
                                       eventname, per_band)).items()
                for sta, sta_meas in measurements:
                    for comp, comp_meas in sta_meas.items():
                        c = comp[-1]
                        w = 0.0
                        try:
                            w = weight[eventname, per_band][comp]["weight"]
                        except KeyError as err:
                            if not comp in str(err):
                                raise err
                            w = 0.0
                        for meas in comp_meas:
                            misfit[per_band][c] += w * meas[misfit_type]
                            pbar.update()

        for p in self.settings['period_bands']:
            for c in "RTZ":
                total_misfit += misfit[p][c]
        
        return total_misfit


    def generate_misfit(self):
        misfit_type = self.settings['misfit_type']
        print(misfit_type)
        misfit = self.generate_misfit_main('weight_file',misfit_type)
        print("Total misfit ("  + misfit_type +  "): ",misfit)
        f=open("fval",'w')
        f.write("%f" % (misfit))
        f.close()

    def generate_misfit_dt_am(self):
        misfit_dt = self.generate_misfit_main('weight_dt_file','misfit_dt')
        print("Total misfit (misfit_dt): ",misfit_dt)
        misfit_am = self.generate_misfit_main('weight_am_file','misfit_dlna')
        print("Total misfit (misfit_dlna): ",misfit_am)
        print("Total misfit : ",misfit_am + misfit_dt)
        f=open("fval",'w')
        f.write("%f" % (misfit_dt + misfit_am))
        f.close()
        
    def generate_weight_dt_and_am_params(self):
        template = self.load_yaml(self.f("weight_template"))
        w_tt, w_amp = self.get_dt_and_am_weights()
        for eventname in self.events:
            ratio = self.get_ratio(eventname)
            ratio = self.extend_ratio_to_dt_and_am(ratio, w_tt, w_amp)
            data = template.copy()
            data["category_weighting"]["ratio"] = ratio
            self.dump_yaml(data, self.f("weight_parfile_dt_am", eventname))


    def generate_weight_dt_and_am_paths(self):
        for eventname in self.events:
            data = {"input": {},
                    "logfile": self.f("weight_log", eventname)}
            for period_band in self.settings["period_bands"]:
                data["input"][period_band+"_DT"] = {
                    "asdf_file": self.f("proc_synt", eventname, period_band),
                    "output_file": self.f("weight_dt_file", eventname, period_band),
                    "station_file": self.f("stations_file", eventname),
                    "window_file": self.f("windows_filter_file", eventname, period_band)
                }
                data["input"][period_band+"_AM"] = {
                    "asdf_file": self.f("proc_synt", eventname, period_band),
                    "output_file": self.f("weight_am_file", eventname, period_band),
                    "station_file": self.f("stations_file", eventname),
                    "window_file": self.f("windows_filter_file", eventname, period_band)
                }

            self.dump_json(data, self.f("weight_path_dt_am", eventname))


    def extend_ratio_to_dt_and_am(self,ratio, w_tt, w_amp):
        new_ratio = {}
        for p in self.settings["period_bands"]:
            p_tt = p+"_DT"
            p_amp = p+"_AM"
            new_ratio[p_tt] = {}
            new_ratio[p_amp] = {}
            for c in ["BHR", "BHT", "BHZ"]:
                new_ratio[p_tt][c] = w_tt*ratio[p][c]
                new_ratio[p_amp][c] = w_amp*ratio[p][c]
        return new_ratio



    def count_windows(self, eventname):
        measurements = {}
        for period_band in self.settings["period_bands"]:
            windows_file = self.f("windows_filter_file", eventname, period_band)  # NOQA
            #print(windows_file)
            windows_data = self.load_json(windows_file)
            #measurements[period_band] = dict((x, 0) for x in ["MXR", "MXT", "MXZ"])  # NOQA
            measurements[period_band] = dict((x, 0) for x in ["BHR", "BHT", "BHZ"])  # NOQA
            for station, components in windows_data.items():
                for component, windows in components.items():
                    c = component.split(".")[-1]
                    measurements[period_band][c] += len(windows)
        return measurements

    def get_ratio(self, eventname):
        counts = self.count_windows(eventname)
        for p in counts:
            for c in counts[p]:
                if counts[p][c] != 0:
                    counts[p][c] = 1 / counts[p][c]
                else:
                    counts[p][c] = 0
        return counts

    def generate_weight_params(self):
        template = self.load_yaml(self.f("weight_template"))
        for eventname in self.events:
            ratio = self.get_ratio(eventname)
            data = template.copy()
            data["category_weighting"]["ratio"] = ratio
            self.dump_yaml(data, self.f("weight_parfile", eventname))

    def generate_weight_paths(self):
        for eventname in self.events:
            data = {"input": {},
                    "logfile": self.f("weight_log", eventname)}
            for period_band in self.settings["period_bands"]:
                data["input"][period_band] = {
                    "asdf_file": self.f("proc_synt", eventname, period_band),
                    "output_file": self.f("weight_file", eventname, period_band),  # NOQA
                    "station_file": self.f("stations_file", eventname),
                    "window_file": self.f("windows_filter_file", eventname, period_band)  # NOQA
                }
            self.dump_json(data, self.f("weight_path", eventname))

    def generate_sum(self):
        for eventname in self.events:
            data = {"input_file": {},
                    "output_file": self.f("sum_adjoint_file", eventname)}
            for period_band in self.settings["period_bands"]:
                data["input_file"][period_band] = {
                    "asdf_file": self.f("adjoint_file", eventname, period_band),  # NOQA
                    "weight_file": self.f("weight_file", eventname, period_band),  # NOQA
                }
            self.dump_json(data, self.f("sum_adjoint_path", eventname))

    def generate_sum_dt_am(self):
        for eventname in self.events:
            data = {"input_file": {},
                    "output_file": self.f("sum_adjoint_file", eventname)}
            for period_band in self.settings["period_bands"]:
                data["input_file"][period_band+"_DT"] = {
                    "asdf_file": self.f("adjoint_file_dt", eventname, period_band),
                    "weight_file": self.f("weight_dt_file", eventname, period_band),
                }
                data["input_file"][period_band+"_AM"] = {
                    "asdf_file": self.f("adjoint_file_am", eventname, period_band),
                    "weight_file": self.f("weight_am_file", eventname, period_band),
                }
            self.dump_json(data, self.f("sum_adjoint_path", eventname))


    def generate_sum_dt_am_q(self):
        for eventname in self.events:
            data = {"input_file": {},
                    "output_file": self.f("sum_adjoint_file_q", eventname)}
            for period_band in self.settings["period_bands"]:
                data["input_file"][period_band+"_DT"] = {
                    "asdf_file": self.f("adjoint_file_dt_q", eventname, period_band),
                    "weight_file": self.f("weight_dt_file", eventname, period_band),
                }
                data["input_file"][period_band+"_AM"] = {
                    "asdf_file": self.f("adjoint_file_am_q", eventname, period_band),
                    "weight_file": self.f("weight_am_file", eventname, period_band),
                }
            self.dump_json(data, self.f("sum_adjoint_path_q", eventname))

    def generate_weight_all(self):
        self.generate_weight_dt_and_am_params()
        self.generate_weight_dt_and_am_paths()

    def generate_adjoint_all(self):
        self.generate_adjoint_am()
        self.generate_adjoint_dt()
        
    def generate_adjoint_q_all(self):
        self.generate_adjoint_am_q()
        self.generate_adjoint_dt_q()

            
    def clean(self):
        print ("Cleaning folders : ")
        command = 'files=$(find .  -type d -name "output");'
        command += 'for ifiles in $files; do rm -rfv "$ifiles/"*; done;'
        subprocess.run(command,shell=True,check=True)
        command = 'files=$(find .  -type d -name "paths");'
        command += 'for ifiles in $files; do rm -rfv "$ifiles/"*; done;'
        subprocess.run(command,shell=True,check=True)
        print ("Cleaning folders : Done")
        

        
        

    def run(self):
        steps = dict([(x[9:], x) for x in dir(self)
                      if x.startswith('generate_')])
        steps["clean"] = "clean"
        
        parser = argparse.ArgumentParser(
            description='Generate path files')
        parser.add_argument('-p', '--paths-file', default="paths.yml")
        parser.add_argument('-s', '--settings-file', default="settings.yml")
        parser.add_argument('-e', '--events-file', default="event_list")
        parser.add_argument("step",  help="file to generate",
                            choices=steps.keys())
        args = parser.parse_args()
        self.folders, self.files = self.load_path_config(args.paths_file)
        self.settings = self.load_yaml(args.settings_file)
        self.events = self.load_events(args.events_file)

        getattr(self, steps[args.step])()


if __name__ == '__main__':
    FileGenerator().run()
