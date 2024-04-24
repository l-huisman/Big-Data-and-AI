<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        
        <div
          :class="{
            'bg-[#D0C27A]': (RowIndex + colIndex) % 2 === 0,
            'bg-[#AA8439]': (RowIndex + colIndex) % 2 !== 0
          }"
          class="w-[60px] h-[60px] p-[10px] flex justify-center items-center">
            <span>
              <img v-if="square !== 0 && dict[RowIndex].hasOwnProperty('black')" :src="getPieceImagePath(square, 'black')" alt="Chess Piece" >
              <img v-else-if="square !== 0  && dict[RowIndex].hasOwnProperty('white')" :src="getPieceImagePath(square, 'white')" alt="Chess Piece" >
            </span>
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
      if(color == 'white') {
        return this.pieceImagesWhite[pieceNumber];
      }
      else {
        return this.pieceImagesBlack[pieceNumber];
      }
    }
  }
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>