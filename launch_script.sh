#!/usr/bin/env bash

# Sets the main.json as default, if the -t is specifed
# it will use that as config file.
configuration_file="main.json"
start_training=1

while getopts ":tlre:w:s:i:" opt; do
    case ${opt} in
        r)
            random=1
            start_training=1
            ;;
        t)
            configuration_file=${OPTARG}
            start_training=1
            ;;
        e)
            environment=${OPTARG}
            start_training=1
            ;;
        w)
            reward=${OPTARG}
            start_training=1
            ;;
        s)
            stop=${OPTARG}
            start_training=1
            ;;
        i)
            iterations=${OPTARG}
            start_training=1
            ;;
        l)
            light=1
            start_training=1
            ;;
    esac
done
shift $((OPTIND -1))
echo "iterations :$iterations"
i=0
if ! [ $iterations ]; then
    iterations=1
fi
while [ $iterations -ne $i ]; do
    if [ $random ]; then
        if [ $environment ]; then
            if [ $light ]; then
                if [ $reward ]; then
                    echo "...creating a random light environment... using $environment and $reward"
                    configuration_file=`python3 env_gen_light.py --environment_file $environment --rewards_file $reward`
                else
                    echo "...creating a  light environment... using $environment"
                    configuration_file=`python3 env_gen_light.py --environment_file $environment --rewards_file "default"`
                fi
            else
                if [ $reward ]; then
                    echo "...creating a random environment... using $environment and $reward"
                    configuration_file=`python3 env_generator.py --environment_file $environment --rewards_file $reward`
                else
                    echo "...creating a random environment... using $environment"
                    configuration_file=`python3 env_generator.py --environment_file $environment --rewards_file "default"`
                fi
            fi
        elif [ $reward ]; then
            echo "...creating a random environment... using $reward"
            configuration_file=`python3 env_generator.py --environment_file "default" --rewards_file $reward`
        else
            echo "...creating a random environment..."
            echo "...creating environment with grid_size 6, number of water tiles 3, max block size 1, with default reward config"
            configuration_file=`python3 env_generator.py --environment_file "default" --rewards_file "default"`
        fi
        configuration_file="randoms/$configuration_file"
    else
        configuration_file=${1:-"main.json"}
    fi

    echo "...environment name is..."
    echo $configuration_file

    if [ $configuration_file -eq "main.json" ]; then
        echo "using default configuration file: $configuration_file"
    else
        echo "...updating selected configuration file..."
        cd ./configurations
        yes | cp -rf $configuration_file "main.json"
        echo "using configuration file: $configuration_file"
    fi

    cd ..

    # Use virtual environment if exists
    if [ -d "venv" ]; then
      echo "...activating python venv..."
      source ./venv/bin/activate
    fi

    echo "...setting up python environment..."
    PYTHONPATH=../gym-minigrid/:../gym-minigrid/gym_minigrid/:./configurations:./:$PYTHONPATH
    export PYTHONPATH

    if ! [ $stop ]; then
        stop=0
    fi

    if [ $start_training -eq 1 ]; then
            echo "...launching the training..."
            echo "+++++ With Controller +++++"
            python3 ./pytorch_rl/main.py --stop $stop --iterations $i
            name=`grep -e '"config_name"' configurations/main.json`
            replace="v0_2\","
            replace=${name/v0\",/$replace}
            sed -i 's/"active": true,/"active": false,/g' configurations/main.json
            sed -i "s/$name/$replace/" configurations/main.json
            echo "\n\n...launching the training..."
            echo "------ Without Controller -----"
            python3 ./pytorch_rl/main.py --stop $stop --iterations $i

    fi
    let "i+=1"

    Rscript plot_result.R
done


# echo "...launch visdom server in the background..."
# python3 -m visdom.server &
