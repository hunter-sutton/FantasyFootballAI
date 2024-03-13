# NFL Player Performance Predictor

An advanced neural network project designed to predict each NFL player's performance using TensorFlow, Keras, and various data manipulation techniques.

## Overview

This project attempts to forecast the performance of individual NFL players by leveraging historical player statistics. The model excludes quarterbacks ("QB") and kickers ("K") due to the unique nature of their scoring and statistics. The project comprises two primary scripts:

- `make_dataset.py`: Handles data retrieval, preprocessing, and export.
- `deep_net.py`: Defines, trains, and evaluates the neural network model using the prepared data.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. Additionally, you will need to install the following packages:

- `numpy`
- `pandas`
- `matplotlib`
- `tensorflow`
- `scikit-learn`
- `requests`
- `tqdm`

You can install these packages using pip:

```
pip install numpy pandas matplotlib tensorflow scikit-learn requests tqdm
```

### Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/your_github_username/NFL-Player-Performance-Predictor.git
```

2. Navigate to the cloned repository's directory:

```
cd NFL-Player-Performance-Predictor
```

## Usage

To generate the dataset and train the model, follow the steps below:

1. **Generate the Dataset**: Run the `make_dataset.py` script to fetch and preprocess the NFL player statistics. This script outputs a `player_stats.csv` file, which serves as input for the neural network model.

```
python make_dataset.py
```

2. **Train the Neural Network**: Execute the `deep_net.py` script, which reads the `player_stats.csv` file, trains the neural network model, and evaluates its performance. The script also produces a graph displaying the model's loss over epochs.

```
python deep_net.py
```

## How It Works

- **Data Collection**: The `make_dataset.py` script fetches player data from the ESPN API, filters inactive players, and retains relevant statistics.
- **Data Preprocessing**: The `deep_net.py` script preprocesses the data by encoding categorical variables, scaling features, and splitting the dataset into training and test subsets.
- **Model Training**: A Sequential model with multiple dense layers and dropout is defined and trained using the processed data.
- **Evaluation**: The model's performance is evaluated against the test dataset to assess its predictive accuracy.

## Contributing

If you'd like to contribute to this project, please feel free to do so. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.