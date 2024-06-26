<template>
  <div class="grid grid-cols-8 ml-30">
    <template v-for="(row, RowIndex) in this.dict" :key="'row-' + RowIndex">
      <template v-for="(square, colIndex) in row" :key="'square-' + colIndex">
        <div :id="RowIndex" @click="changeClickToMove(RowIndex)"
          :class="{ 'hover:bg-[#b0a468] bg-[#D0C27A]': getSquareColors(RowIndex), 'hover:bg-[#8a6b2d] bg-[#AA8439]': !getSquareColors(RowIndex) }"
          class="w-[60px] h-[60px] pt-[10px] pb-[10px] flex justify-center items-center">

          <!-- show the numbers on the left side of the aowboard -->
          <div v-if="RowIndex % 8 == 0" class="text-sm mb-auto mr-auto pl-[4px] mt-[-8px]" :class="{
            'text-[#D0C27A]': !getSquareColors(RowIndex), 'text-[#AA8439]': getSquareColors(RowIndex)
          }">{{ (RowIndex /
            8) + 1 }}</div>
          <div v-else class="text-sm mb-auto mr-auto pl-[4px] mt-[-8px]">&nbsp;</div>

          <!-- show the aowboard + pieces -->
          <span>
            <img v-if="square !== 0 && dict[RowIndex].hasOwnProperty('black')"
              :src="getPieceImagePath(square, 'black')">
            <img v-else-if="square !== 0 && dict[RowIndex].hasOwnProperty('white')"
              :src="getPieceImagePath(square, 'white')" alt=".">
          </span>

          <!-- show the letters on the bottom of the aowboard -->
          <div v-if="RowIndex >= 56" class="text-sm mt-auto ml-auto pr-[4px] mb-[-9px]" :class="{
            'text-[#D0C27A]': !getSquareColors(RowIndex),
            'text-[#AA8439]': getSquareColors(RowIndex)
          }">{{ String.fromCharCode(RowIndex + 9).toLowerCase() }}</div>
          <div v-else class="text-sm mt-auto ml-auto pr-[4px] mb-[-9px]">&nbsp;</div>
        </div>
      </template>
    </template>
  </div>
</template>


<script>
import { baseUrl } from '../base-url.js';

export default {
  props: {
    board: Array,
    isAIGame: Boolean,
    cardId: Number,
  },
  data() {
    return {
      gameBoard: this.board,
      dict: [],
      whitePieces: [],
      blackPieces: [],
      possibleMoves: [],
      position: '',
      pieceImagesWhite: {
        1: '/_nuxt/assets/images/pieces/pawn white.png',
        2: '/_nuxt/assets/images/pieces/bishop white.png',
        3: '/_nuxt/assets/images/pieces/knight white.png',
        4: '/_nuxt/assets/images/pieces/rook white.png',
        5: '/_nuxt/assets/images/pieces/queen white.png',
        6: '/_nuxt/assets/images/pieces/king white.png',
        7: '/_nuxt/assets/images/pieces/winged_hussar white.png',
        8: '/_nuxt/assets/images/pieces/hoplite white.png',
        9: '/_nuxt/assets/images/pieces/war_elephant white.png',
      },
      pieceImagesBlack: {
        1: '/_nuxt/assets/images/pieces/pawn black.png',
        2: '/_nuxt/assets/images/pieces/bishop black.png',
        3: '/_nuxt/assets/images/pieces/knight black.png',
        4: '/_nuxt/assets/images/pieces/rook black.png',
        5: '/_nuxt/assets/images/pieces/queen black.png',
        6: '/_nuxt/assets/images/pieces/king black.png',
        7: '/_nuxt/assets/images/pieces/winged_hussar black.png',
        8: '/_nuxt/assets/images/pieces/hoplite black.png',
        9: '/_nuxt/assets/images/pieces/war_elephant black.png',
      }
    };
  },
  mounted() {
    this.blackPieces = this.gameBoard[0];
    this.whitePieces = this.gameBoard[1].reverse();
    this.createDict();
  },
  methods: {
    async changeClickToMove(index) {
      if (this.isAIGame) {
        return;
      }
      const row = Math.floor(index / 8) + 1;
      const column = String.fromCharCode(97 + (index % 8));
      const position = column + row;

      if (this.cardId == 1) {
        if (this.checkForWaterlineMove(position)){
          this.$emit('position-clicked', this.position);
          this.position = '';
          return;
        }
      }

      this.position = this.position + position;
      this.possibleMoves = await this.calculatePossibleMoves(this.position);
      if(this.cardId == 0 || this.cardId == 3 || this.cardId == 4){
        this.position = this.position + this.position;
      }
      else if (this.position.length === 2) {
        return;
      }

      if (!this.possibleMoves.includes(this.position)) {
        this.position = position;
        this.calculatePossibleMoves(position);
        this.colorSquares();
      } else {
        this.$emit('position-clicked', this.position);
        this.position = '';
      }

    },
    async calculatePossibleMoves(move) {
      let position = move.charAt(0) + move.charAt(1);
      this.gameBoard[1].reverse();
      const response = await fetch(`${baseUrl}/actions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          board: this.gameBoard,
          turn: 1,
          pieceLocation: position
        })
      }).catch(error => {
        console.error('Error:', error);
      });
      this.gameBoard[1].reverse();
      const data = await response.json();
      return this.color(data, position);
    },
    color(data, position) {
      for (let move of data.possibleMoves) {
        this.colorPossibleMoves(move);
      }

      if (this.position.length == 4) {
        if (!data.possibleMoves.includes(position)) {
          this.colorSquares();
        }
      }
      return data.possibleMoves;
    },
    createDict() {
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
    checkForWaterlineMove(position) {
      if (position == 'a3') {
        this.position = 'a6h8';
      }
      else if (position == 'a4') {
        this.position = 'a5h8';
      }
      else if (position == 'a5') {
        this.position = 'a4h8';
      }
      else if (position == 'a6') {
        this.position = 'a3h8';
      } else {
        return false;
      }
      return true;
    },
    getPieceImagePath(pieceNumber, color) {
      if (color == 'white') {
        return this.pieceImagesWhite[pieceNumber];
      }
      else {
        return this.pieceImagesBlack[pieceNumber];
      }
    },
    getSquareColors(num) {
      const specialNumbers = [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22, 25, 27, 29, 31, 32, 34, 36, 38, 41, 43, 45, 47, 48, 50, 52, 54, 57, 59, 61, 63];
      return specialNumbers.includes(num);
    },
    colorPossibleMoves(move) {
      const column = move.charAt(2);
      const row = parseInt(move.charAt(3)) - 1;
      const index = row * 8 + (column.charCodeAt(0) - 97);
      document.getElementById(index).style.border = '#000 2px solid';
    },
    colorSquares() {
      for (let i = 0; i < 64; i++) {
        document.getElementById(i).style.border = '#000 0px solid'
      }
    },
  }
};
</script>

<style scoped>
body {
  background-color: #3B6651;
}
</style>