<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        <div :class="{
          'bg-[#D0C27A]': GetSquareColors(RowIndex),
          'bg-[#AA8439]': !GetSquareColors(RowIndex)
        }" class="w-[60px] h-[60px]  pt-[10px] pb-[10px] flex justify-center items-center">
        <div v-if="RowIndex == 0" class="text-[#AA8439] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">1</div>
        <div v-else-if="RowIndex == 8" class="text-[#D0C27A] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">2</div>
        <div v-else-if="RowIndex == 16" class="text-[#AA8439] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">3</div>
        <div v-else-if="RowIndex == 24" class="text-[#D0C27A] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">4</div>
        <div v-else-if="RowIndex == 32" class="text-[#AA8439] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">5</div>
        <div v-else-if="RowIndex == 40" class="text-[#D0C27A] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">6</div>
        <div v-else-if="RowIndex == 48" class="text-[#AA8439] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">7</div>
        <div v-else-if="RowIndex == 56" class="text-[#D0C27A] text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">8</div>
        <div v-else class="text-sm mb-auto mr-auto pl-[4px] mt-[-8px]" :class="{
          'text-[#D0C27A]': GetSquareColors(RowIndex),
          'text-[#AA8439]': !GetSquareColors(RowIndex)
        }">1</div>
          <span>
            <img v-if="square !== 0 && dict[RowIndex].hasOwnProperty('black')" :src="getPieceImagePath(square, 'black')"
              alt="Chess Piece">
            <img v-else-if="square !== 0 && dict[RowIndex].hasOwnProperty('white')"
              :src="getPieceImagePath(square, 'white')" alt="Chess Piece">
          </span>

        <div v-if="RowIndex == 56" class="text-[#D0C27A] text-sm mt-auto ml-auto  pr-[5px] mb-[-9px]">a</div>
        <div v-else-if="RowIndex == 57" class="text-[#AA8439] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">b</div>
        <div v-else-if="RowIndex == 58" class="text-[#D0C27A] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">c</div>
        <div v-else-if="RowIndex == 59" class="text-[#AA8439] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">d</div>
        <div v-else-if="RowIndex == 60" class="text-[#D0C27A] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">e</div>
        <div v-else-if="RowIndex == 61" class="text-[#AA8439] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">f</div>
        <div v-else-if="RowIndex == 62" class="text-[#D0C27A] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">g</div>
        <div v-else-if="RowIndex == 63" class="text-[#AA8439] text-sm mt-auto ml-auto pr-[5px] mb-[-9px]">h</div>
        <div v-else class="text-sm mb-auto mr-auto pl-[4px] mt-[-7px] pr-[5px] mb-[-9px]" :class="{
          'text-[#D0C27A]': GetSquareColors(RowIndex),
          'text-[#AA8439]': !GetSquareColors(RowIndex)
        }">1</div>
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
      ],
      pieceImagesWhite: {
        1: '/_nuxt/assets/images/pieces/pawn white.png',
        2: '/_nuxt/assets/images/pieces/bishop white.png',
        3: '/_nuxt/assets/images/pieces/knight white.png',
        4: '/_nuxt/assets/images/pieces/rook white.png',
        5: '/_nuxt/assets/images/pieces/queen white.png',
        6: '/_nuxt/assets/images/pieces/king white.png',
      },
      pieceImagesBlack: {
        1: '/_nuxt/assets/images/pieces/pawn black.png',
        2: '/_nuxt/assets/images/pieces/bishop black.png',
        3: '/_nuxt/assets/images/pieces/knight black.png',
        4: '/_nuxt/assets/images/pieces/rook black.png',
        5: '/_nuxt/assets/images/pieces/queen black.png',
        6: '/_nuxt/assets/images/pieces/king black.png',
      }
    };
  },
  mounted() {
    const first64 = this.gamestate.slice(0, 8);
    const last64 = this.gamestate.slice(8).reverse();

    for (let i = 0; i < first64.length; i++) {
      for (let j = 0; j < first64[i].length; j++) {
        if (first64[i][j] != 0) {
          this.dict.push({
            'white': first64[i][j]
          });
        }
        else if (last64[i][j] != 0) {
          this.dict.push({
            'black': last64[i][j]
          });
        }
        else {
          this.dict.push({
            'Empty': first64[i][j]
          });
        }

      }
    }
  },

  methods: {
    getPieceImagePath(pieceNumber, color) {
      if (color == 'white') {
        return this.pieceImagesWhite[pieceNumber];
      }
      else {
        return this.pieceImagesBlack[pieceNumber];
      }
    },
    GetSquareColors(num) {
      const specialNumbers = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50, 52, 54, 57, 59, 61, 63];
      return specialNumbers.includes(num);
    }
  }
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>