 #!/bin/bash

for f in paths/*.path.json
do
    pypaw-convert_to_asdf -f $f -v -s
done
