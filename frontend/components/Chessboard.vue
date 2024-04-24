<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        
        <div
          :class="{
            'bg-[#D0C27A]': (RowIndex + colIndex) % 2 === 0,
            'bg-[#AA8439]': (RowIndex + colIndex) % 2 !== 0
          }"
          class="w-[70px] h-[70px] flex justify-center items-center">
          <span class="text-white">{{ square }}</span>
<!-- <img src="../../chess/pieces/__pycache__/bishop.cpython-311.pyc" alt="not work"> -->
        </div>
      </template>
    </template>
  </div>
</template> 


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
            // color: 'white',
            'white': first64[i][j]
          });
        }
        else if (last64[i][j] != 0) {
          this.dict.push({
            // color: 'black',
            'black': last64[i][j]
          });
        }
        else {
          this.dict.push({ 
            // color: 'Empty',
            'Empty': first64[i][j]
          });
        }

      }
    }

    console.log(this.dict);
  },
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>