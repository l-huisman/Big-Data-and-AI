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
          <!-- <span class="text-white">{{ square }}</span> -->
            <span>
              <img v-if="square !== 0" :src="getPieceImagePath(square)" alt="Chess Piece" class="w-full h-full absolute inset-0 w-[40px] h-[40px]">
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
      pieceImages: {
        1: '/_nuxt/assets/images/pieces/pawn black.png',
        2: '/_nuxt/assets/images/pieces/rook black.png',
        3: '/_nuxt/assets/images/pieces/knight black.png',
        4: '/_nuxt/assets/images/pieces/bishop black.png',
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
            // key: 'white',
            // value: first64[i][j]
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

    console.log(this.dict);
  },

  methods: {
    getPieceImagePath(pieceNumber) {
      return this.pieceImages[pieceNumber];
    }
  }
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>