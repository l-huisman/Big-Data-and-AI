<template>
  <div class="flex h-screen w-screen mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <Chessboard />
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]" >
      <div class=" text-2xl mb-[10px]">
        <div>Turn 1</div>
      </div>
      <div class="flex flex-row bg-[#afe0c8] rounded-[5px] border-[7px] border-[#5a9679]">
        <div class="w-1/2">
          <Line height="200px" :data="chartData" :options="chartOptions"></Line>
          <Line height="200px" :data="chartData1" :options="chartOptions1"></Line>
        </div>
        <div class="w-1/2">
          <Pie id="pie-chart" :options="pieChartOptions" :data="pieChartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';
import axios from 'axios';

import { Line, Pie } from 'vue-chartjs'
import Chart from 'chart.js/auto';

export default {
  components: {
    Chessboard,
    Line,
    Pie
  },
  data() {
    return {
      //win chances
      chartData: {
        labels: ['January', 'February', 'March', 'January', 'February'],
        datasets: [
          { data: [40, 20, 10, 40, 20,], label: 'White', borderColor: '#567cb8' },
          { data: [30, 50, 10, 40, 10], label: 'Black', borderColor: '#94979c' }
        ]
      },
      chartOptions: {
        plugins: {
          title: {
            display: true,
            text: 'Win chances per turn',
          }
        },
        responsive: true,
        scales: {
          x: {
            type: 'category',
            labels: ['January', 'February', 'March', 'January', 'February'],
            title: {
              display: true,
              text: 'Turns',
            }
          },
          y: {
            min: 0,
            max: 100,
            title: {
              display: true,
              text: '%',
            }
          }
        }
      },
      //total rewards per turn
      chartData1: {
        labels: ['January', 'February', 'March', 'January', 'February'],
        datasets: [
          { data: [40, 20, 10, 40, 20,], label: 'White', borderColor: '#567cb8' },
          { data: [30, 50, 10, 40, 10], label: 'Black', borderColor: '#94979c' }
        ]
      },
      chartOptions1: {
        plugins: {
          title: {
            display: true,
            text: 'Total rewards per turn',
          }
        },
        responsive: true,
        scales: {
          x: {
            type: 'category',
            labels: ['January', 'February', 'March', 'January', 'February'],
            title: {
              display: true,
              text: 'Turns',
            }
          },
          y: {
            min: -300,
            max: 300,
            title: {
              display: true,
              text: 'Rewards',
            }
          }
        }
      },
      //total of checks
      pieChartData: {
        labels: ['White', 'Black'],
        datasets: [{
          data: [70, 30],
          backgroundColor: ['#567cb8', '#94979c']
        }]
      },
      pieChartOptions: {
        plugins: {
          title: {
            display: true,
            text: 'Total of checks',
          }
        },
        responsive: true
      },
      turn: 1,
      imageRows: [
        ['hoplite', 'hoplite', 'hoplite'],
        ['winged knight', 'dutch waterline', 'war elefant']
      ]
    };
  },
  methods: {
    getImageUrl(imageName) {
      return require(`../assets/images/${imageName}.png`);
    }
  }
};


</script>

<style>
body {
  background-color: #3B6651;
}
</style>