# Workflow test

# Running the tests

You can generate a script from the instructions below using
`generate_run_script.sh`. Then you can run the created `run.sh` file.


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

	$ python generate_path_files.py measure

and then run the script

	$ cd measure
	$ ./run_measureadj.sh
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


## Calculate weights


Generate param files (We need to count windows to generate these)

	$ python generate_path_files.py weight_params

Generate path files

	$ python generate_path_files.py weight_paths


and then run the script

	$ cd weights
	$ ./calc_weights.sh
	$ cd ..


## Sum adjoint sources


Generate path files

	$ python generate_path_files.py sum

and then run the script

	$ cd sum_adjoint
	$ ./sum_adjoint.sh
	$ cd ..
