for file in configs/pl_*
do
    for i in `seq 1 2`
    do
        srun --partition=common --qos=2gpu1d --gres=gpu:1 python probing/run_experiment.py $file --train-probe=1
    done
done