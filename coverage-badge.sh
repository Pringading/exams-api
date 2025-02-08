#!/usr/bin/env bash

COVERAGE=$(coverage report --format=total)

if [ $COVERAGE -lt 50 ]; then
    COLOUR="red"
elif [ $COVERAGE -lt 60 ]; then
    COLOUR="tomato"
elif [ $COVERAGE -lt 70 ]; then
    COLOUR="orange"
elif [ $COVERAGE -lt 80 ]; then
    COLOUR="yellow"
elif [ $COVERAGE -lt 85 ]; then
    COLOUR="greenyellow"
elif [ $COVERAGE -lt 95 ]; then
    COLOUR="green"
else
    COLOUR="forestgreen"
fi

