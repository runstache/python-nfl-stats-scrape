input_week=1
input_year=$1
input_type=2



while [ $input_week -lt 18 ]; do
  echo "Pulling games for $input_year week $input_week"
  command="python stats_loader.py -w $input_week -y $input_year -t $input_type"
  eval $command
  ((input_week+=1))
done
