mkdir -p data/raw/$2

for file in $1*.conllu
do
    split="${file##*-}" # everything after the last -
    split="${split%.*}" # everyting up to the dot
    filename="data/raw/$2/$split.txt"
    python scripts/convert_conll_to_raw.py $file > $filename
    head -n 1 $filename
done