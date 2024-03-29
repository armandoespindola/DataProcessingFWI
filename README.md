# Workflow test

# Environment setup

Batch scripts contain slurm headers and mpirun calls.

Number cpu cores per node and account name (can be blank) can be set by running
`setup_scripts.sh` script.

# Running the tests

You can generate a script from the instructions below using
`generate_run_script.sh`. Then you can run the created `run.sh` file.


Get misfit type

	$ misfit=$(grep ^misfit settings.yml | cut -d: -f2 | xargs)
	$ misfit_prefix=${misfit/'misfit_'/}
	$ echo "#########"
	$ echo "misfit: "$misfit
	$ echo "prefix: "$misfit_prefix
	$ bash setup_scripts.sh "" 2 "" "" "" "" "mpirun -n" 1
	
## Setup

First generate needed folders by

	$ python generate_path_files.py folders


## Convert sac files to ASDF

Generate path files

	$ python generate_path_files.py converter


and then run the script

	$ cd converter
	$ ./convert_to_asdf.sh
	$ cd ..

## Process asdf

Generate path files

	$ python generate_path_files.py proc


and then run the script

	$ cd proc
	$ ./run_preprocessing.sh
	$ cd ..


## Select windows


Generate path files

	$ python generate_path_files.py windows

and then run the script

	$ cd windows
	$ ./select_windows.sh
	$ cd ..


## Calculate measures


Generate path files

	$ python generate_path_files.py measure_all

and then run the script

	$ cd measure
	$ ./run_measureadj_${misfit_prefix}.sh
	$ cd ..


## Generate station.json files


Generate path files

	$ python generate_path_files.py stations

and then run the script

	$ cd stations
	$ ./extract_stations.sh
	$ cd ..


## Filter windows


Generate path files

	$ python generate_path_files.py filter

and then run the script

	$ cd filter
	$ ./filter_windows.sh
	$ cd ..


## Calculate adjoints


Generate path files

	$ python generate_path_files.py adjoint_all

and then run the script

	$ cd adjoint
	$ bash "run_pyadj_${misfit_prefix}.sh"
	$ cd ..



## Calculate weights


Generate param files (We need to count windows to generate these)
Generate path files

	$ python generate_path_files.py weight_all


and then run the script

	$ cd weights
	$ bash "calc_weights_${misfit_prefix}.sh"
	$ cd ..


## Sum adjoint sources


Generate path files

	$ python generate_path_files.py sum_all

and then run the script

	$ cd sum_adjoint
	$ ./sum_adjoint.sh
	$ cd ..


# Running workflow for a different data set

## Edit settings.yml

Modify:
- period_bands
- data_components
- tag obsd
- tag synt
- misfit_type (misfit_dt,misfit_am,misfit_dt_am)


## Edit parfiles

Edit:
- proc: proc/parfile/<tag>.<period>.param.yml
- windows windows/parfile/window.<period>.param.yml (Please check test example!)
- measure/run_measureadj_<misfit>.<period>.sh.template
- adjoint adjoint/parfile/multitaper.adjoint_<misfit>.<period>.config.yml
- weights weights/parfile/template.window_weights.param.yml
- sum_adjoint sum_adjoint/parfile/sum_adjoint.param.yml