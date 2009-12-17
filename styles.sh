#!/bin/sh

if [ x$1 == x ]; then
    echo "please supply destination path as argument"
    exit
fi

STYLES=$(pygmentize -L styles|awk '/\*/ { sub(":$", ""); print $2 }')

for style in $STYLES
do
    pygmentize -f html -S $style > $1/$style.css
done
