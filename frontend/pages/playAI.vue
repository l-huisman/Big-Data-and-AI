<template>
  <div class="flex h-screen w-screen mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <Chessboard :board="board" :key="boardKey" />
      <!-- <Chessboard :board="board" @update:board="newState" /> -->
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]">
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
        <button @click="fetchGameAIvsAI(fmodel, smodel), setupCharts()"
          class="w-full rounded-full bg-[#3B6651] p-2">Start AI
          game</button>
      </div>
      <div class="flex flex-row bg-[#afe0c8] rounded-[20px] border-[10px] border-[#5a9679]">
        <div class="w-1/2">
          <div id="reward-chart" style="width: 100%; height: 300px;"></div>
        </div>
        <div class="w-1/2">
          <!-- <div id="reward-chart2" style="width: 100%; height: 300px;"></div> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';
import * as echarts from 'echarts';
import { baseUrl } from '../base-url.js';

export default {
  components: {
    Chessboard,
  },
  data() {
    return {
      fmodel: 'PPO',
      smodel: 'PPO',
      rewardChart: null,
      rewards: [],
      boardKey: 0,
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
  mounted() {
    this.setupCharts();
  },
  methods: {
    async fetchGameAIvsAI(white_model, black_model) {
      const response = await fetch(`${baseUrl}/aigame`, {
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
      this.runAIvsAI(data.game, data.statistics);
    },
    async runAIvsAI(game, stats) {
      for (let i = 1; i < game.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.makeMove(game[i]);
        this.updateCharts(stats[i]);
      }
    },
    makeMove(board) {
      this.board[0].reverse();

      this.board[1] = board[1];
      this.boardKey++;

      setTimeout(() => {
        this.board[0] = board[0];
        this.boardKey++;
      }, 2000);
    },
    setupCharts() {
      var chartDom = document.getElementById('reward-chart');
      this.rewardChart = echarts.init(chartDom);
      var option;

      option = {
        xAxis: {
          type: 'category',
          data: ['1', '10', '20', '30', '40', '50', '100']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Reward White',
            data: [0],
            type: 'line'
          },
          {
            name: 'Reward Black',
            data: [0],
            type: 'line'
          }
        ]
      };

      option && this.rewardChart.setOption(option);
    },
    updateCharts(stats) {
      console.log(stats)
      this.rewardChart.setOption({
        series: [
          {
            name: 'Reward White',
            data: [stats["rewards"][0]],
            type: 'line'
          },
          {
            name: 'Reward Black',
            data: [stats["rewards"][1]],
            type: 'line'
          }
        ]
      });
      
      // work in progress currently the chart is updating but just shows the last value this was a fix but did not work so i commented it out
      // this.rewardsWhite.push(stats["rewards"][0]);
      // this.rewardsBlack.push(stats["rewards"][1]);
      // this.rewardChart.setOption({
      //   series: [
      //     {
      //       name: 'Reward White',
      //       data: [this.rewardsWhite.values],
      //       type: 'line'
      //     },
      //     {
      //       name: 'Reward Black',
      //       data: [this.rewardsBlack],
      //       type: 'line'
      //     }
      //   ]
      // });
    }
  }
};


</script>

<style>
body {
  background-color: #3B6651;
}
</style>