for SEED in 0 1 2
do
    for file in configs/all_slavic/pl_hr*.yaml
    do
        srun --partition=common --qos=2gpu1d --gres=gpu:1 python probing/run_experiment.py $file --train-probe=1 --seed=$SEED --randomize=1

    done

    # for file in configs/missing_slavic/pl*.yaml
    # do
    #     srun --partition=common --qos=2gpu1d --gres=gpu:1 python probing/run_experiment.py $file --train-probe=1 --seed=$SEED --randomize=1

    # done
done