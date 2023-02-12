#!/bin/bash
rm temp.gif out.gif
convert $1 -coalesce temp.gif
convert -size $2 temp.gif -resize 32x32 out.gif
