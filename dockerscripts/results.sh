#!/usr/bin/env bash

sudo docker exec -t $(sudo docker ps -lq) mkdir -p /headless/gym-minigrid/results
dir -p /headless/gym-minigrid
echo "Launching plot scripts in all the running containers..."
sudo docker exec -t $(sudo docker ps -lq) python3 plotResult.py
echo "...done"
echo ""


echo "Extracting the plot folder from all the running containers..."
for pid in `sudo docker ps -q`; do
	sudo docker cp $pid:/headless/gym-minigrid/results ~/results
done
echo "...done"
echo ""

exit