#!/usr/bin/env bash

# Sets the main.json as default, if the -t is specifed
# it will use that as config file.
configuration_file="main.json"
start_training=1
qlearning=0
double=0
launch_monitor=0
launch_without=0

while getopts qrt:e:w:s:i:lab opt; do
    case ${opt} in
        q)
            qlearning=1
            ;;
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
        a)
            launch_monitor=1
            ;;
        b)
            launch_without=1
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
    fi

    echo "...environment name is..."
    echo $configuration_file

    if [ $configuration_file -eq "main.json" ]; then
        echo "using default configuration file: $configuration_file"
        cd ./configurations
    else
        echo "...updating selected configuration file..."
        cd ./configurations
        echo "using configuration file: $configuration_file"
        yes | cp -rf $configuration_file "main.json"
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
    echo $launch_monitor

    if [ $start_training -eq 1 ]; then
            echo "...launching the training..."
            if [ $launch_monitor -eq 1 ]; then
                echo "+++++ With Controller +++++"
                if [ $qlearning -eq 1 ]; then
                    echo "launching: ./pytorch_dqn/main.py --stop $stop --record"
                    python3 ./pytorch_dqn/main.py --stop $stop --record --norender
                else
                    python3 ./pytorch_a2c/main.py --stop $stop --record --norender
                fi
            fi
            if [ $launch_without -eq 1 ]; then
                name=`grep -e '"config_name"' configurations/main.json`
                replace="v0_2\","
                replace=${name/v0\",/$replace}
                sed -i 's/"active": true,/"active": false,/g' configurations/main.json
                sed -i "s/$name/$replace/" configurations/main.json
                echo "..launching the training..."
                echo "------ Without Controller -----"
                if [ $qlearning -eq 1 ]; then
                    python3 ./pytorch_dqn/main.py --stop $stop --record --norender --nomonitor
                else
                    python3 ./pytorch_a2c/main.py --stop $stop --record --norender --nomonitor
                fi
            fi
            echo "plotting..."
            python3 ./evaluations/a2c/plot_dqn.py
            python3 ./evaluations/a2c/plot_a2c.py
    fi
    let "i+=1"

done


