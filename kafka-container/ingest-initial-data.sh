#!/bin/bash
file=$(cat $@)


for line in $file
do
    echo "$line"
    echo "$line" | kafka-console-producer --broker-list localhost:29094 --topic foo
done