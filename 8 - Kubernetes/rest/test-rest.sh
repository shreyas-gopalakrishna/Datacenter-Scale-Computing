#!/bin/sh

export ip="$1"
echo "Running test against host $ip"

if [ ! [ping -c 1 $ip ] ];
then
    echo
fi

for img in ../images/*;
do
    echo "Send $img"
    python rest-client.py $ip image $img 1
done

echo "Get plates of image with valid plate"
curl http://$ip:5000/hash/786d4d75e52cde3b292045265aa59a2c
echo ""

echo "Get plates of image with no valid plate"
curl http://$ip:5000/hash/1acb43b6af19e8d90ea94d40f5b8e207
echo ""

echo "Get hash of known plate"
curl http://$ip:5000/license/7B9SJLD
echo ""