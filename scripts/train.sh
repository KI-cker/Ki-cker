#!/bin/bash

rm -r images
mkdir images
rm -r model
mkdir model

for a in $(seq 0.00005 0.0001 0.00085)
do
    mkdir "images/$a"
    mkdir "model/$a"
    j=1
    while [ $j -le 2 ]
    do
        i=1
        while [ $i -le 50 ]
        do
            python tools/train_1000.py -g 0.99 -l $a && cp model_new.h5 model.h5 && echo 'Finished run nr. '$i &&let i=$i+1
            sleep 30s
        done

        python tools/image_viewer.py -c $(($j*50)) -f $a
        let j=$j+1
    done
    cp model.h5 "model/$a/model_after_100_training_runs.h5"
    rm model.h5
done