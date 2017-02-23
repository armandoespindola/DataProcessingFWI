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

	$ cd windows
	$ ./run_measureadj.sh

