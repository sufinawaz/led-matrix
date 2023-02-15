#!/bin/bash
sourceFile=$1
sourceRes=`identify -format '%w %h' $1[0] | tr ' ' 'x'`
rm temp1.gif out1.gif
convert $sourceFile -coalesce temp1.gif
convert -size $sourceRes temp1.gif -resize 64x32! out1.gif
