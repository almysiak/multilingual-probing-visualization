for dir in /home/amysiak/thesis/multilingual-probing-visualization/data/raw/*/
do
    echo "$dir"
    lang="${dir%/}"             # strip trailing slash (if any)
    lang="${lang##*/}"
    output_dir="/home/amysiak/thesis/multilingual-probing-visualization/data/hdf5/$lang"
    mkdir -p $output_dir

    for file in $dir*
    do
        split="${file##*/}"
        split="${split%.*}"
        output="$output_dir/$split.hdf5"
        # echo "$output"
        python /home/amysiak/thesis/multilingual-probing-visualization/scripts/convert_raw_to_bert.py $file $output $1 $lang
    done
done
