# Workflow test

## Setup

First generate needed folders by

	$ python generate_path_files.py folders


## Convert sac files to ASDF

Generate path files

	$ python generate_path_files.py folders


and then run the script

	$ cd converter
	$ ./convert_to_asdf.sh
