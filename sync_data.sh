#!/usr/bin/env bash

if [ "$1" = "down" ]; then
	echo "Fetching data from ADA"
	rsync -ah --info=progress2 ada:/share3/ishaanshah/volsdf /ssd_scratch/cvit/ishaan/
	rsync -ah --info=progress2 ada:/share3/ishaanshah/volsdf_data /ssd_scratch/cvit/ishaan/
fi

if [ "$1" = "up" ]; then
	echo "Uploading data to ADA"
	rsync -ah --info=progress2 /ssd_scratch/cvit/ishaan/volsdf ada:/share3/ishaanshah/
	rsync -ah --info=progress2 /ssd_scratch/cvit/ishaan/volsdf_data ada:/share3/ishaanshah/
fi
