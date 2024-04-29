<template>
  <div class="flex h-screen w-screen mt-[155px] text-white">
    <div class="ml-[10%] text-2xl">
      <Chessboard />
    </div>
    <div class="ml-[50px] flex flex-col w-[45%]">
      <div class=" text-2xl mb-[10px]">
        <div>Turn 1</div>
      </div>
      <div class="flex flex-row bg-[#f2f2f2] rounded-[5px] border-[10px] border-[#f2f2f2]">
        <div class="w-[50%]" >
          <Line :data="chartData" :options="chartOptions"></Line>
          <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
        </div>
        <div class="w-[50%]">
          <Pie id="pie-chart" :options="pieChartOptions" :data="pieChartData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';
import axios from 'axios';

import { Bar, Line, Pie } from 'vue-chartjs'
import Chart from 'chart.js/auto';

export default {
  components: {
    Chessboard,
    Bar,
    Line,
    Pie
  },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March'],
        datasets: [{ data: [40, 20, 12] }]
      },
      chartOptions: {
        responsive: true,
        scales: {
          x: {
            type: 'category',
            labels: ['January', 'February', 'March'],
          },
          y: {
            min: 0,
            max: 50
          }
        }
      },
      lineChartData: {
        labels: ['January', 'February', 'March'],
        datasets: [{
          label: 'My Line Dataset',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          data: [30, 40, 50]
        }]
      },
      lineChartOptions: {
        responsive: true,
        scales: {
          x: {
            type: 'category',
            labels: ['January', 'February', 'March'],
          },
          y: {
            min: 0,
            max: 60
          }
        }
      },
      pieChartData: {
        labels: ['Red', 'Blue', 'Yellow'],
        datasets: [{
          data: [30, 20, 50],
          backgroundColor: ['pink', 'lightblue', 'lightgrey']
        }]
      },
      pieChartOptions: {
        responsive: true
      },
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