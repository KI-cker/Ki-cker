#!/bin/bash

while getopts l:t: option
do
case "${option}"
in
l) learning_rate=${OPTARG};;
t) training_iterations=${OPTARG};;
esac
done

i=1
while [ $i -le $training_iterations ]
do
    python tools/train_1000.py -g 0.99 -l $learning_rate && cp model_new.h5 model.h5 && echo 'Finished run nr. '$i &&let i=$i+1
    sleep 30s
done