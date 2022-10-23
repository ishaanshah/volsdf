#!/usr/bin/env bash
#SBATCH -A research
#SBATCH -n 10
#SBATCH -N 1
#SBATCH --partition long
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=4-00:00:00
#SBATCH --output=object_logs.txt
#SBATCh --constraint='2080ti|2080ti,phase3'

set -e

source notify

bash sync_data.sh down

source "/home2/ishaanshah/miniconda3/etc/profile.d/conda.sh"
conda activate /ssd_scratch/cvit/ishaan/volsdf

cd code
python training/exp_runner.py --conf ./confs/stic.conf  --expname hand_test

bash sync_data.sh up
