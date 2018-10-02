#!/usr/bin/env bash

# Sets the main.json as default, if the -t is specifed
# it will use that as config file.
configuration_file="main.json"
environment="default"
reward="default"
start_training=1
qlearning=0
double=0
launch_monitor=0
launch_without=0
logstdfile=0
plot=0

while getopts qt:r:e:w:s:i:labfp opt; do
    case ${opt} in
        q)
            qlearning=1
            ;;
        r)
            random=1
            random_iterations=${OPTARG}
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
        f)
            logstdfile=1
            ;;
        p)
            plot=1
            ;;
    esac
done
shift $((OPTIND -1))
i=0
if ! [ $iterations ]; then
    iterations=1
fi
echo "iterations :$iterations"

if ! [ $random_iterations ]; then
    random_iterations=1
fi
echo "random iterations :$random_iterations"

while [ $random_iterations -ne $i ]; do
    if [ $random ]; then
        if [ $light ]; then
            echo "...creating a random light environment... using environment_file: $environment and reward_file: $reward"
            configuration_file=`python3 env_gen_light.py --environment_file $environment --rewards_file $reward`
        else
            echo "...creating a random environment... using $environment and $reward"
            configuration_file=`python3 env_generator.py --environment_file $environment --rewards_file $reward`
        fi
        configuration_file="randoms/$configuration_file"
    fi
    j=0
    while [ $iterations -ne $j ]; do
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

        chmod 744 ./pytorch_dqn/main.py
        chmod 744 ./pytorch_a2c/main.py

        if [ $start_training -eq 1 ] && [ $logstdfile -eq 0 ]; then
        echo "...launching the training without logging to file..."
                if [ $launch_monitor -eq 1 ]; then
                    echo "+++++ With Envelope +++++"
                    if [ $qlearning -eq 1 ]; then
                        echo "launching: ./pytorch_dqn/main.py --stop $stop "
                        python3 ./pytorch_dqn/main.py --stop $stop  --norender
                    else
                        echo "launching ./pytorch_a2c/main.py --stop $stop  --norender"
                        python3 ./pytorch_a2c/main.py --stop $stop  --norender
                    fi
                fi
                if [ $launch_without -eq 1 ]; then
                    echo "------ Without Envelope -----"
                    if [ $qlearning -eq 1 ]; then
                        echo "launching: ./pytorch_dqn/main.py --stop $stop "
                        python3 ./pytorch_dqn/main.py --stop $stop  --norender --nomonitor
                    else
                        echo "launching: ./pytorch_a2c/main.py --stop $stop  --norender --nomonitor"
                        python3 ./pytorch_a2c/main.py --stop $stop  --norender --nomonitor
                    fi
                fi
                if [ $plot -eq 1 ]; then
                    echo "plotting..."
                    python3 ./evaluations/plot_dqn.py
                    python3 ./evaluations/plot_single.py
                fi
        fi
        if [ $start_training -eq 1 ] && [ $logstdfile -eq 1 ]; then
        echo "...launching the training logging to file..."
                if [ $launch_monitor -eq 1 ]; then
                    echo "+++++ With Envelope +++++"
                    if [ $qlearning -eq 1 ]; then
                        echo "launching: ./pytorch_dqn/main.py --stop $stop "
                        python3 ./pytorch_dqn/main.py --stop $stop  --norender --logstdfile
                    else
                        echo "launching: ./pytorch_a2c/main.py --stop $stop  --norender --logstdfile"
                        python3 ./pytorch_a2c/main.py --stop $stop  --norender --logstdfile
                    fi
                fi
                if [ $launch_without -eq 1 ]; then
                    echo "------ Without Envelope -----"
                    if [ $qlearning -eq 1 ]; then
                        echo "launching: ./pytorch_dqn/main.py --stop $stop  --norender --nomonitor --logstdfile"
                        python3 ./pytorch_dqn/main.py --stop $stop  --norender --nomonitor --logstdfile
                    else
                        echo "launching: ./pytorch_a2c/main.py --stop $stop  --norender --nomonitor --logstdfile"
                        python3 ./pytorch_a2c/main.py --stop $stop  --norender --nomonitor --logstdfile
                    fi
                fi
                if [ $plot -eq 1 ]; then
                    echo "plotting..."
                    python3 ./evaluations/plot_dqn.py
                    python3 ./evaluations/plot_single.py
                fi
        fi
        let j+=1
    done
    let "i+=1"
done


