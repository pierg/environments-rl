
This is an extension of ["Minimalistic Gridworld Environment for OpenAI Gym"
](https://github.com/maximecb/gym-minigrid)


Requirements:
- Python 3.6
- Pip3
- [PyTorch for Python 3.6 ](https://pytorch.org)


Then with pip3 install the required packages:

```
pip3 install -r requirements.txt
```

If launching from terminal, first export the python environment:

```
PYTHONPATH=../gym-minigrid/:../gym-minigrid/gym_minigrid/:./configurations:./:$PYTHONPATH
export PYTHONPATH
```

Then you can launch the agent manually:

```
python3 ./launch_agent_manual.py
```

Launch the training with a2c:

```
python3 ./pytorch_a2c/main.py
```


## Configuration file

The configuration file in 'configurations/main.json' is used by all the project through all the training.
It specifies all the importat variables needed to configure an experiment such as:

1. Name of the environment
2. Rewards to be assigned to the agent
3. Monitors to activate and their conditions
4. Parameters of the training algorithm

Modify main.json to launch the configuration that you want.

All the results of the training will be saved in the 'evaluations' folder

## Launching experiments with the launch_script.sh

You can easily launch training sessions by launching the launch_script.sh

The available options are:

*-t* configuration file to choose for training (located in configurations folder)
If no configuration file is specified configurations/main.json is used

*-q* to train with DQN

*-r* to activate the random environment generation

*-l* to use the random light generator

*-e env_filename* specifies the configuration of the random environment generator (located in configurations/environments)
If no file is specified configurations/environments/default.json is used

*-w reward_filename* specifies the reward file to be used in the random environment generator (located in configurations/rewards)
If no file is specified configurations/rewards/default.json is used

*-s stop_steps* overrides from the configuration file the max number of steps to train the agent

*-i iteration_number* specifies the number of iterations, meaning the number of times to run the same configuration

*-f* save output in a LOG.txt file

*-a* launch the training with the safety envelope

*-b* launch the training without the safety envelope


### Examples of experiments that can be launched

Launch configurations/light_test_1.json with the safety envelope
```
./launch_script.sh -t light_test_1.json -a
```

Launch configurations/light_test_1.json without the safety envelope
```
./launch_script.sh -t light_test_1.json -b
```

Launch configurations/light_test_1.json first with and then without the safety envelope
```
./launch_script.sh -t light_test_1.json -a -b
```

Launch configurations/main.json first with and then without the safety envelope
```
./launch_script.sh -a -b
```

Generate a random environment with a light switch using configurations/environments/env_config.json as environment configuration and configurations/environments/reward_config as rewards configuration. Then launch the training on the generated environment first with and then without the safety envelope
```
./launch_script.sh -r -l -e env_config -w reward_config -a -b
```


### Docker
The easiest way to launch an experiment and collect results is with docker.
You can pull the image from dockerhub:
```
docker pull pmallozzi/gym-minigrid:patterns
```

All the arguments passed to the docker image when running it will be passed to the launch_script.sh

For example you can run:
```
docker run -it -v ~/evaluations/:/headless/gym-minigrid/evaluations pmallozzi/gym-minigrid:patterns -a -b -t light_test_2.json
```