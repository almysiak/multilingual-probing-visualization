lang=$1
# lang="${dir%/}"             # strip trailing slash (if any)
# lang="${lang##*/}"
dir="/home/amysiak/thesis/multilingual-probing-visualization/data/raw/$lang"
output_dir="/home/amysiak/thesis/multilingual-probing-visualization/data/hdf5/$lang"
mkdir -p $output_dir

for file in $dir/*
do
    split="${file##*/}"
    split="${split%.*}"
    output="$output_dir/$split.hdf5"
    # echo "$output"
    python /home/amysiak/thesis/multilingual-probing-visualization/scripts/convert_raw_to_bert.py $file $output multilingual $lang
done
