now=$(date)
srun --partition=common --qos=2gpu1d --gres=gpu:1 python probing/run_experiment.py /home/amysiak/thesis/multilingual-probing-visualization/configs/all_slavic/cs_de_10000.yaml  --train-probe=1 --seed=99
echo $now
date