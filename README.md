## Art of War: Big Data & AI School Project

This repository contains a Python project implementing a variant of the game "Art of War" with special moves and trained
using Proximal Policy Optimization (PPO) and Deep Q-learning (DQN) algorithms.

The project was created for the Big Data & AI school project at InHolland, Minot.

### Gameplay

This version of Art of War includes:

* Standard chess mechanics
* Special moves activated by cards:
    * Hoplites
    * War Elephant
    * Winged Knight
    * Dutch Waterline

It's not advisable to include every single Windows and Linux command in the README file as it would be overwhelming and
irrelevant to the project's specific needs. However, we can enhance the existing instructions to be more user-friendly
across both operating systems:

### Running the Project

**Prerequisites:**

* Python 3 (Download from [https://www.python.org/downloads/](https://www.python.org/downloads/))
* Required libraries (install using `pip install -r requirements.txt`)

**Installation:**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your_username>/art-of-war-ai.git  # Replace with your repo URL
   ```

2. **Install dependencies:**

    * **Linux/macOS:**

      ```bash
      cd art-of-war-ai  # Navigate to project directory
      pip3 install -r requirements.txt
      ```

    * **Windows:**

      ```bash
      cd art-of-war-ai  # Navigate to project directory
      pip install -r requirements.txt
      ```

**Training the Models:**

* Open a terminal or command prompt and navigate to the project directory.
* Train the PPO model (replace `<model_name>` with `dqn` or `ppo` to train their respective models):
    * **Linux/macOS:**

     ```bash
     python3 train.py <model_name>
     ```

    * **Windows:**

     ```bash
     py train.py <model_name>
     ```

* Training parameters can be adjusted in the `args` dictionary within `train.py`.

**Plotting Training Results:**

* Run the following to generate graphs for each training run in a separate directory.
    ```bash 
    python3 plot.py
    ```

**Playing Against the AI:**

* Run the following to challenge the trained AI model. Moves can be made from the console.
    ```bash 
    python3 play.py
    ```

**AI vs. AI Match:**

* Run `python3 modeltest.py <model_name>`where `<model_name>` is either `ppo` or `dqn` to observe the models compete
  against each other.
