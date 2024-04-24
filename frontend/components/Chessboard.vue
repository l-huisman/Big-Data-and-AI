<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        <div :class="{ 'bg-[#D0C27A]': GetSquareColors(RowIndex), 'bg-[#AA8439]': !GetSquareColors(RowIndex) }"
          class="w-[60px] h-[60px] pt-[10px] pb-[10px] flex justify-center items-center">

          <!-- show the numbers on the left side of the chessboard -->
          <div v-if="RowIndex % 8 == 0" class="text-sm mb-auto mr-auto pl-[4px] mt-[-8px]" :class="{
            'text-[#D0C27A]': !GetSquareColors(RowIndex), 'text-[#AA8439]': GetSquareColors(RowIndex)
          }">{{ (RowIndex /
            8) + 1}}</div>
          <div v-else class="text-sm mb-auto mr-auto pl-[4px] mt-[-8px]" :class="{
            'text-[#D0C27A]': GetSquareColors(RowIndex),
            'text-[#AA8439]': !GetSquareColors(RowIndex)
          }">1</div>

          <!-- show the chessboard + pieces -->
          <span>
            <img v-if="square !== 0 && dict[RowIndex].hasOwnProperty('black')" :src="getPieceImagePath(square, 'black')"
              alt="Chess Piece">
            <img v-else-if="square !== 0 && dict[RowIndex].hasOwnProperty('white')"
              :src="getPieceImagePath(square, 'white')" alt="Chess Piece">
          </span>

          <!-- show the letters on the bottom of the chessboard -->
          <div v-if="RowIndex >= 56" class="text-sm mt-auto ml-auto pr-[4px] mb-[-9px]" :class="{
            'text-[#D0C27A]': !GetSquareColors(RowIndex),
            'text-[#AA8439]': GetSquareColors(RowIndex)
          }">{{ String.fromCharCode(RowIndex + 9).toLowerCase() }}</div>
          <div v-else class="text-sm mt-auto ml-auto pr-[4px] mb-[-9px]" :class="{
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
      whitePieces: [],
      blackPieces: [],
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
    this.SplitGamestate();
    this.CreateDict();
  },

  methods: {
    SplitGamestate() {
      this.whitePieces = this.gamestate.slice(0, 8);
      this.blackPieces = this.gamestate.slice(8).reverse();
    },
    CreateDict() {
      for (let i = 0; i < this.whitePieces.length; i++) {
        for (let j = 0; j < this.whitePieces[i].length; j++) {
          if (this.whitePieces[i][j] != 0) {
            this.dict.push({
              'white': this.whitePieces[i][j]
            });
          }
          else if (this.blackPieces[i][j] != 0) {
            this.dict.push({
              'black': this.blackPieces[i][j]
            });
          }
          else {
            this.dict.push({
              'Empty': this.whitePieces[i][j]
            });
          }

        }
      }
    },
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