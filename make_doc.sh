#!/bin/sh

epydoc --config epydoc.config

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
        #echo "The regex matches!"
        prefix=${BASH_REMATCH[1]}
    fi
    rm $i
    mv $prefix.$name-class.html $i 
  	#echo "$i"
done