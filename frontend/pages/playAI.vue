<template>
  <div class="flex h-screen w-screen mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <Chessboard :board="board" />
      <!-- <Chessboard :board="board" @update:board="newState" /> -->
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]" >
      <div class=" text-2xl mb-[10px]">
        <div>Turn 1</div>
      </div>
      <div class="flex flex-row bg-[#5a9679] rounded-[5px] border-[7px] border-[#5a9679] mb-2">
        <select v-model="fmodel" class="bg-[#5a9679]" name="firstmodel" id="firstmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
        </select>
        <select v-model="smodel" class="bg-[#5a9679]" name="secondmodel" id="secondmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
        </select>
        <button @click="fetchGameAIvsAI(fmodel, smodel)" class="w-full rounded-full bg-[#3B6651] p-2">Start AI game</button>
      </div>
      <div class="flex flex-row bg-[#afe0c8] rounded-[5px] border-[7px] border-[#5a9679]">
        <div class="w-1/2">
          <!-- <Line height="200px" :data="chartData" :options="chartOptions"></Line> -->
          <!-- <Line height="200px" :data="chartData1" :options="chartOptions1"></Line> -->
        </div>
        <div class="w-1/2">
          <!-- <Pie id="pie-chart" :options="pieChartOptions" :data="pieChartData" /> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';

export default {
  components: {
    Chessboard,
  },
  data() {
    return {
      fmodel: 'PPO',
      smodel: 'PPO',
      newState: [],
      board: [[
                    [4, 3, 2, 6, 5, 2, 3, 4],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [4, 3, 2, 6, 5, 2, 3, 4],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
                ],
    }

  },
  methods: {
    async fetchGameAIvsAI(white_model, black_model) {
      const response = await fetch('http://127.0.0.1:8000/aigame', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          white_model: white_model,
          black_model: black_model
        })
      });
      const data = await response.json();
      console.log(data);
      this.runAIvsAI(data.game);
    },
    // not working yet
    runAIvsAI(game) {
      for (let i = 1; i < game.length; i++) {
        setTimeout(() => {
          this.newState = game[i];
        }, 1000);
      }
    }
  }
};


</script>

<style>
body {
  background-color: #3B6651;
}
</style>