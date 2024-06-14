<template>
  <div>
    <button class="w-[100px] text-white rounded-full bg-[#5a9679] p-2 m-4" @click="goBack()"><-</button>
  </div>
  <div class="flex h-full w-full mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <aowboard :board="board" :key="boardKey" :isAIGame="true" />
      <!-- <aowboard :board="board" @update:board="newState" /> -->
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]">
      <div class="flex flex-row bg-[#5a9679] rounded-[5px] border-[7px] border-[#5a9679] mb-2">
        <select v-if="!gameIsActive" v-model="fmodel" class="bg-[#5a9679]" name="firstmodel" id="firstmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
          <option value="A2C">A2C</option>
        </select>
        <select v-if="!gameIsActive" v-model="smodel" class="bg-[#5a9679]" name="secondmodel" id="secondmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
          <option value="A2C">A2C</option>
        </select>
        <Button id="start-button" type="button" @click="fetchGameAIvsAI(fmodel, smodel), setupCharts()" 
          class="w-full rounded-full bg-[#3B6651] p-2"><span v-if="loading"> <i class="fa fa-spinner fa-spin"></i> Loading</span><span v-else-if="this.gameIsActive">{{ this.fmodel }} is playing against {{ this.smodel }}</span><span v-else> Start AI
          game</span></Button>
      </div>
      <div class="flex flex-row bg-[#afe0c8] rounded-[20px] border-[10px] border-[#5a9679]">
        <div class="w-1/2">
          <div id="reward-chart" style="width: 100%; height: 300px; padding-top: 20px;"></div>
        </div>
        <div class="w-1/2">
          <div id="summary-reward-chart" style="width: 100%; height: 300px; padding-top: 20px;"></div>
        </div>
      </div>
      <div>
        <div v-if="!gameIsActive" class="ml-4 mt-4 text-2xl">
          <div> {{this.winner}}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import aowboard from '../components/aowboard.vue';
import * as echarts from 'echarts';
import { baseUrl } from '../base-url.js';

export default {
  components: {
    aowboard,
  },
  data() {
    return {
      rewardsList: [[0,0], [0,0], [0,0], [0,0], [0,0]],
      totalRewardsList: [[0,0], [0,0], [0,0], [0,0], [0,0]],
      totalRewards: [0, 0],
      loading: false,
      gameIsActive: false,
      winner: "",
      fmodel: 'PPO',
      smodel: 'PPO',
      rewardChart: null,
      summaryRewardChart: null,
      rewards: [],
      boardKey: 0,
      board: [[
        [4, 3, 2, 5, 6, 2, 3, 4],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      [
        [4, 3, 2, 5, 6, 2, 3, 4],
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
      this.gameIsActive = true; 
      this.loading = true;
      document.getElementById("start-button").disabled = "true";

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
      
      this.checkWinner(data);
      this.runAIvsAI(data.game, data.statistics);
      this.loading = false;
    },
    checkWinner(data) {
      if(data.winner == 'Draw'){
        this.winner = 'The game ended in a draw!';
      }
      else {
        this.winner = data.winner + ' has won the game!';
      }
    },
    async runAIvsAI(game, stats) {
      for (let i = 1; i < game.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.makeMove(game[i]);
        this.updateCharts(stats[i]);
      }
      this.gameIsActive = false;
      document.getElementById("start-button").removeAttribute('disabled');
      
    },
    makeMove(board) {
      this.board = board;
      this.boardKey++;
    },
    getOptions(title){
      return {
        title: {
          text: title,
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: ['5', '4', '3', '2', '1']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Reward Black',
            data: [0],
            type: 'line',
            color : 'black'
          },
          {
            name: 'Reward White',
            data: [0],
            type: 'line',
            color : 'white'
          }
        ]
      };
    },
    setupCharts() {
      let chartDom = document.getElementById('reward-chart');
      this.rewardChart = echarts.init(chartDom);
      let optionR = this.getOptions("Rewards per move");
      optionR && this.rewardChart.setOption(optionR);

      let chartDomSummary = document.getElementById('summary-reward-chart');
      this.summaryRewardChart = echarts.init(chartDomSummary);
      let optionSR = this.getOptions("Total rewards");
      optionSR && this.summaryRewardChart.setOption(optionSR);
    },
    updateCharts(stats) {
      let rewardsList = this.updateRewardsList(stats);
      this.updateChart(rewardsList, this.rewardChart);

      let totalRewards = this.updateTotalRewards(stats);
      this.updateChart(totalRewards, this.summaryRewardChart);
    },
    updateChart(list, chart){
      chart.setOption({
        series: [
          {
            name: 'Reward Black',
            data: [list[0][0], list[1][0], list[2][0], list[3][0], list[4][0]],
            type: 'line'
          },
          {
            name: 'Reward White',
            data: [list[0][1], list[1][1], list[2][1], list[3][1], list[4][1]],
            type: 'line'
          }
        ]
      });
    },
    updateRewardsList(stats) {
      this.rewardsList.push(stats["rewards"]);
      if (this.rewardsList.length > 5) {
        this.rewardsList.shift();
      }
      return this.rewardsList;
    },
    updateTotalRewards(stats) {
      this.totalRewards[0] = stats["rewards"][0] + this.totalRewards[0];
      this.totalRewards[1] = stats["rewards"][1] + this.totalRewards[1];
      let reward = [this.totalRewards[0], this.totalRewards[1]];
      this.totalRewardsList.push(reward);
      if (this.totalRewardsList.length > 5) {
        this.totalRewardsList.shift();
      }
      return this.totalRewardsList;
    },
    goBack() {
      this.$router.push('/');
    }
  }
};


</script>

<style>
body {
  background-color: #3B6651;
}
</style>