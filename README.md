## Art of War: Big Data & AI School Project

This repository contains a Python project implementing a variant of the game "Art of War" with special moves and trained
using Proximal Policy Optimization (PPO), Advantage Actor Critic (A2C) and Deep Q-learning (DQN) algorithms.

The project was created for the Big Data & AI school Minor at InHolland.

### Gameplay

This version of Art of War includes:

* Standard aow mechanics
* Special moves activated by cards:
    * Hoplites
    * War Elephant
    * Winged Knight
    * Dutch Waterline

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
      
    **Note:** Make sure to first start the virtual environment if you are using one. For more info on venv, see [here](https://docs.python.org/3/library/venv.html).


**Training the Models:**

* Open a terminal or command prompt and navigate to the project directory.
* Train the PPO model (replace `<model_name>` with `dqn`, `a2c` or `ppo` to train their respective models):
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
**Ai vs. AI:**

* Run the following to run a local environment where 2 ppo alchoritms play agains eacother.
    ```bash 
    python3 aivsai.py
    ```

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

### Starting the Front-end
* Open a terminal or command prompt and navigate to the project directory.
* First navigate to the frontend directory and install all packages by running the command:

    ```bash
    cd frontend
    npm install
    ```

* Then you can run it in dev mode by using the following command:

    ```bash
    npm run dev
    ```

* It will generate a link which is, if not already taken: [`http://127.0.0.1:3000`](http://127.0.0.1:3000/)

