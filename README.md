# NFL Player Performance Predictor

This project features a neural network designed to predict the performance of NFL players. Additionally, it includes tools for visualizing data from your own fantasy football league, allowing users to analyze player performance and team dynamics comprehensively.

## Overview

`deep_net.py` - A script that processes player data and feeds it into a neural network to predict individual NFL player performance.

`make_dataset.py` - This script retrieves player data from ESPN and processes it into a usable format for analysis and machine learning models.

`fantasy.py` - Contains the `Fantasy` class used to fetch and analyze fantasy football league data, including plotting functions for various statistical analyses.

`main.py` - A graphical user interface (GUI) application built with Tkinter for easy use of the data visualization tools provided by the `Fantasy` class.

## Installation

To run this project, you'll need Python installed on your system along with the following packages:

- Tensorflow
- Keras
- Pandas
- NumPy
- Matplotlib
- Sklearn
- Requests
- tqdm
- espn_api

You can install all required packages using pip:

```sh
pip install tensorflow keras pandas numpy matplotlib sklearn requests tqdm espn_api
```

## Usage

### Training the Neural Network

1. Prepare your data in `player_stats.csv` file within the same directory. This should include the statistics of NFL players that you want to analyze.
2. Run `deep_net.py` to train the model based on your data.
   ```sh
   python deep_net.py
   ```

### Generating the Dataset

1. Use `make_dataset.py` to retrieve and process player data from ESPN. This script saves the processed data to `player_stats.csv`, which `deep_net.py` uses for model training.
   ```sh
   python make_dataset.py
   ```

### Fantasy Football League Analysis

1. Customize `league_id`, `year`, `espn_s2`, and `swid` in `fantasy.py` with your league's details.
2. Run `main.py` to start the GUI application for visualizing data.
   ```sh
   python main.py
   ```

Through the GUI, you can:
- Plot average position ranks of starters or entire team.
- Visualize the standard deviation of position ranks and scores.
- Examine scores over time for all teams or a specific team.

## Contributing

Contributions to this project are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.