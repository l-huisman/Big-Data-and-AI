<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, rowIndex) in 8" :key="'row-' + rowIndex">
      <template v-for="(square, colIndex) in 8" :key="'square-' + colIndex">
        <div :class="{
          'bg-[#D0C27A]': (rowIndex + colIndex) % 2 === 0,
          'bg-[#AA8439]': (rowIndex + colIndex) % 2 !== 0
        }" class="w-[65px] h-[65px] flex justify-center items-center">
          <span class="text-white">{{ square }}</span>
        </div>
      </template>
    </template>
  </div>
</template>


<!-- <template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        
        <div
          :class="{
            'bg-[#D0C27A]': (RowIndex + colIndex) % 2 === 0,
            'bg-[#AA8439]': (RowIndex + colIndex) % 2 !== 0
          }"
          class="w-[70px] h-[70px] flex justify-center items-center">
          <span class="text-white">{{ this.dict[RowIndex].value }}</span>
        </div>
      </template>
    </template>
  </div>
</template>  -->

<!-- square = white 4 -->
<!-- colIndex = key value -->
<!-- row = { key: white} -->
<!-- rowIndex = i -->

<script>
export default {
  data() {
    return {
      dict: [],
      numbers: [1, 2, 3, 4, 5, 6, 7, 8],
      gamestate: [
        [4, 3, 2, 5, 6, 2, 3, 4],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [4, 3, 2, 5, 6, 2, 3, 4],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    };
  },
  mounted() {
    const first64 = this.gamestate.slice(0, 8);
    const last64 = this.gamestate.slice(8).reverse();

    for (let i = 0; i < first64.length; i++) {
      for (let j = 0; j < first64[i].length; j++) {
        if (first64[i][j] != 0) {
          this.dict.push({
            color: 'white',
            number: first64[i][j]
          });
        }
        else if (last64[i][j] != 0) {
          this.dict.push({
            color: 'black',
            number: last64[i][j]
          });
        }
        else {
          this.dict.push({ 
            color: 'Empty',
            number: first64[i][j]
          });
        }

      }
    }

    console.log(this.dict[0, 1]);
  },
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>