#!/bin/bash

printf '\n'
echo "#---------------------------------------------------------------------------------------------------------------#"
echo "#Developed by Erin Zaborowski                                                                                   #"
echo "#Last Updated 10/04/2021                                                                                        #"
echo "#  -updated section: ALL                                                                                        #"
echo "#                                                                                                               #"
echo "#---------------------------------------------------------------------------------------------------------------#"

cluster_config.sh fetch 

sourceDir=/Users/erin.zaborowski/Documents/Source_Files/Professional_Services/PROJECTS/Endo_Pharm
cluster=

slide1parameters=("cluster_name" "")

slide1parameters=("cluster_name" "")

slide1parameters=("cluster_name" "")

#Iterate through parameters to output values to screen.

echo "Slide 1 Parameters" >> parameters.json

for i in "${slide1parameters[@]}"
    do
        slide1=$(grep $i $source/$cluster/cluster_config) | python -m json.tool >> $source/$cluster/$cluster-parameters.json 

        echo $slide1



