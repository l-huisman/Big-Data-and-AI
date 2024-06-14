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
   git clone https://github.com/l-huisman/Big-Data-and-AI.git
   ```

2. **Install dependencies:**

    * **Linux/macOS:**

      ```bash
      cd Big-Data-and-AI/backend  # Navigate to project directory
      pip3 install -r requirements.txt
      ```

    * **Windows:**

      ```bash
      cd Big-Data-and-AI/backend  # Navigate to project directory
      pip install -r requirements.txt
      ```

   **Note:** Make sure to first start the virtual environment if you are using one. For more info on venv,
   see [here](https://docs.python.org/3/library/venv.html).

**Training the Models:**

* Open a terminal or command prompt and navigate to the project directory.
* Train the PPO model (replace `<model_name>` with `dqn` or `ppo` or `a2c` to train their respective models):
    * **Linux/macOS:**

     ```bash
     python3 train.py <model_name>
     ```

    * **Windows:**

     ```bash
     py train.py <model_name>
     ```

* Training parameters can be adjusted in the `args` dictionary within `train.py`.

**Playing Against the AI:**

* Run the following to challenge the trained AI model. Moves can be made from the console.
    ```bash 
    python3 play.py
    ```

**AI vs. AI Match:**

* Run `python3 test.py <model_name>`where `<model_name>` is either `ppo` or `dqn` or `a2c` to observe the models compete
  against each other.

## FastAPI Integration

This project includes a FastAPI to interact with the trained AI models.

### Starting the API

1. **Make sure you have trained a model.**
2. Open a terminal or command prompt and navigate to the project directory.
3. Start the API using Uvicorn:

   ```bash
    cd backend # Navigate to the backend directory
    uvicorn api.main:app --reload
   ```

4. The API will be available at [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/).

**Note:** 
  * Replace `8000` with the port number specified in `uvicorn` if different.
  * Uvicorn should be installed with the requirements but if not, you may need to install `uvicorn` using `pip install uvicorn`.

### API Routes

All api router can be found in the Swagger UI at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

