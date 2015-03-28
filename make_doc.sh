#!/bin/sh

epydoc --config epydoc.config -v

# rm YAAS.controller.DeviceController-module.html
# mv YAAS.controller.DeviceController.DeviceController-class.html  YAAS.controller.DeviceController-module.html

for i in ./resources/api/YAAS*-module.html
  do
  	echo "search in $i"
    if [[ $i =~ ([^.]*)-module ]]
      then
        name=${BASH_REMATCH[1]}
    fi
    if [[ $i =~ (.*)[^.]*-module ]]
      then
        echo "The regex matches!"
        prefix=${BASH_REMATCH[1]}
    fi
    if [ -s $prefix.$name-class.html ]
      then
      	echo "Rename $prefix.$name-class.html to $i"
        rm $i
        mv $prefix.$name-class.html $i
    fi 
  	#echo "$i"
done