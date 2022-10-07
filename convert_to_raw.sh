mkdir -p /home/amysiak/thesis/multilingual-probing-visualization/data/raw/$2
mkdir -p /home/amysiak/thesis/multilingual-probing-visualization/data/conllu/$2

for file in $1*.conllu
do
    split="${file##*-}" # everything after the last -
    split="${split%.*}" # everyting up to the dot
    filename="/home/amysiak/thesis/multilingual-probing-visualization/data/raw/$2/$split.txt"
    conllu_filename="/home/amysiak/thesis/multilingual-probing-visualization/data/conllu/$2/$split.conllu"
    python /home/amysiak/thesis/multilingual-probing-visualization/scripts/convert_conll_to_raw.py $file > $filename
    cp $file $conllu_filename
    head -n 1 $filename
done