<template>
  <div>
    <button class="w-[100px] text-white rounded-full bg-[#5a9679] p-2 m-4" @click="goBack()"><-</button>
  </div>
  <div class="flex h-full w-full mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <Chessboard :board="board" :key="boardKey" />
      <!-- <Chessboard :board="board" @update:board="newState" /> -->
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]">
      <div class="flex flex-row bg-[#5a9679] rounded-[5px] border-[7px] border-[#5a9679] mb-2">
        <select v-model="fmodel" class="bg-[#5a9679]" name="firstmodel" id="firstmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
        </select>
        <select v-model="smodel" class="bg-[#5a9679]" name="secondmodel" id="secondmodel">
          <option value="PPO">PPO</option>
          <option value="DQN">DQN</option>
        </select>
        <Button id="start-button" type="button"  @click="fetchGameAIvsAI(fmodel, smodel), setupCharts()" 
          class="w-full rounded-full bg-[#3B6651] p-2"><span v-if="loading"> <i class="fa fa-spinner fa-spin"></i> Loading</span><span v-else> Start AI
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
      rewardsList: [[0,0], [0,0], [0,0], [0,0], [0,0]],
      totalRewardsList: [[0,0], [0,0], [0,0], [0,0], [0,0]],
      totalRewards: 0,
      loading: false,
      fmodel: 'PPO',
      smodel: 'PPO',
      rewardChart: null,
      summaryRewardChart: null,
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
      console.log(data);
      this.runAIvsAI(data.game, data.statistics);
      this.loading = false;
    },
    async runAIvsAI(game, stats) {
      for (let i = 1; i < game.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.makeMove(game[i]);
        this.updateCharts(stats[i]);
      }
      console.log("Game finished");
      document.getElementById("start-button").removeAttribute('disabled');
    },
    makeMove(board) {
      this.board = board;
      this.boardKey++;
    },
    setupCharts() {
      var chartDom = document.getElementById('reward-chart');
      this.rewardChart = echarts.init(chartDom);
      var optionR;

      optionR = {
        title: {
          text: 'Rewards per move',
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
      optionR && this.rewardChart.setOption(optionR);

      var chartDomSummary = document.getElementById('summary-reward-chart');
      this.summaryRewardChart = echarts.init(chartDomSummary);
      var optionSR;

      optionSR = {
        title: {
          text: 'Total rewards',
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

      optionSR && this.summaryRewardChart.setOption(optionSR);
    },
    updateCharts(stats) {
      var rewardsList = this.updateRewardsList(stats);
      this.rewardChart.setOption({
        series: [
          {
            name: 'Reward White',
            data: [rewardsList[0][0], rewardsList[1][0], rewardsList[2][0], rewardsList[3][0], rewardsList[4][0]],
            type: 'line'
          },
          {
            name: 'Reward Black',
            data: [rewardsList[0][1], rewardsList[1][1], rewardsList[2][1], rewardsList[3][1], rewardsList[4][1]],
            type: 'line'
          }
        ]
      });

      let totalRewards = this.updateTotalRewards(stats);

      this.summaryRewardChart.setOption({
        series: [
          {
            name: 'Reward White',
            data: [totalRewards[0][0], totalRewards[1][0], totalRewards[2][0], totalRewards[3][0], totalRewards[4][0]],
            type: 'line'
          },
          {
            name: 'Reward Black',
            data: [totalRewards[0][1], totalRewards[1][1], totalRewards[2][1], totalRewards[3][1], totalRewards[4][1]],
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
      // this.totalRewards += stats["rewards"][0] + stats["rewards"][1];
      // this.totalRewardsList.push(this.totalRewards);
      this.rewardsList.push(stats["rewards"]);
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