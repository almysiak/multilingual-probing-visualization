for SEED in 0 1 2 3
do
    for file in configs/all_slavic/*.yaml
    do
        srun --partition=common --qos=2gpu1d --gres=gpu:1 python probing/run_experiment.py $file --train-probe=1 --seed=$SEED
    done
done