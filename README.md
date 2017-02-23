# Workflow test

## Setup

First generate needed folders by

	$ python generate_path_files.py folders


## Convert sac files to ASDF

Generate path files

	$ python generate_path_files.py converter


and then run the script

	$ cd converter
	$ ./convert_to_asdf.sh

## Process asdf

Generate path files

	$ python generate_path_files.py proc


and then run the script

	$ cd proc
	$ ./run_preprocessing.sh


## Select windows


Generate path files

	$ python generate_path_files.py windows

and then run the script

	$ cd windows
	$ ./select_windows.sh


## Calculate measures


Generate path files

	$ python generate_path_files.py measure

and then run the script

	$ cd measures
	$ ./run_measureadj.sh


## Generate station.json files


Generate path files

	$ python generate_path_files.py stations

and then run the script

	$ cd stations
	$ ./extract_stations.sh


## Filter windows


Generate path files

	$ python generate_path_files.py filter

and then run the script

	$ cd filter
	$ ./filter_windows.sh


## Calculate weights


Generate param files (We need to count windows to generate these)

	$ python generate_path_files.py weight_params

Generate path files

	$ python generate_path_files.py weight_paths


and then run the script

	$ cd weights
	$ ./calc_weights.sh

