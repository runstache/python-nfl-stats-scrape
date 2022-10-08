input_week=$2
input_year=$1
input_type=$4
max_week=$3

while [ $input_week -lt $max_week ]; do
  echo "Pulling games for $input_year week $input_week"
  command="python schedule_loader.py -w $input_week -y $input_year -t $input_type"
  eval $command
  ((input_week+=1))
done