<template>
    <div class="grid grid-cols-8 ml-30">
      <template v-for="(row, rowIndex) in chessboard" :key="'row-' + rowIndex">
        <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
          <div
            :class="{
              'bg-[#D0C27A]': (rowIndex + colIndex) % 2 === 0,
              'bg-[#AA8439]': (rowIndex + colIndex) % 2 !== 0
            }"
            class="w-[65px] h-[65px] flex justify-center items-center">
            <span class="text-white">{{ square }}</span>
          </div>
        </template>
      </template>
    </div>
</template>

<script>
export default {
  data() {
    return {
      chessboard: [
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
      ]
    };
  }
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>
