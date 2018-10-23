#!/bin/bash

rm -r images
mkdir images

j=1

while [ $j -le 4 ]
do
    i=1
    while [ $i -le 25 ]
    do
        python tools/train_1000.py
        echo 'Finished run nr. '$i
        let i=$i+1
        sleep 15s
    done

    python tools/image_viewer.py
    cp model.h5 models/model.h5
done

