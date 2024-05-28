<template>
    <div class="flex justify-center w-screen mt-[155px] text-white">
       <div class="cards-container ai-opponent mt-[10px]" style="top: 0%;">
        <div class="background-container mt-[-70px]" style="transform: scaleY(-1);">
                <img src="https://artofwargame.io/wp-content/uploads/2023/07/MainMenuPanelFrameTop.png" alt="frame" class="">
                <img src="https://artofwargame.io/wp-content/uploads/2023/07/MainMenuPanelFrameTop.png" alt="frame" class="mirror-image">

  </div>
          <div v-for="(row, index) in imageRows" :key="index" class="flex flex-row justify-end">
             <div v-for="(image, imageIndex) in row" :key="imageIndex" class="ml-[-40px] ">
                <img :src="getImageUrl('cards', 'cardback')" alt="not working" class="h-[165px] mb-[10px] card" :class="{ 'selected': selectedImageIndex === index + (imageIndex * 3) }" id="card"/>
             </div>
          </div>
       </div>
       <div class="mt-[50px] text-2xl">
        <Deployment />
          <Chessboard :board="move_request.board" :key="boardKey" @position-clicked="handlePositionClicked" @position-confirmed="handlePositionConfirmed" class="mx-auto w-full"/>
        <Decks />
       </div>
       <div>
          <div class="cards-container player" style="bottom: 0%;">
            <div class="background-container mt-[30px]">

                <img src="https://artofwargame.io/wp-content/uploads/2023/07/MainMenuPanelFrameTop.png" alt="frame" class="">
                <img src="https://artofwargame.io/wp-content/uploads/2023/07/MainMenuPanelFrameTop.png" alt="frame" class="mirror-image">

  </div>
             <div v-for="(row, index) in imageRows" :key="index" class="flex flex-row justify-end">
                <div v-for="(image, imageIndex) in row" :key="imageIndex" class="ml-[-40px] ">
                   <img :src="getImageUrl('cards', image)" alt="not working" class="h-[165px] mb-[10px] card" :class="{ 'selected': selectedImageIndex === index + (imageIndex * 3) }" id="card" @click="handleImageClick(index + (imageIndex * 3))"/>
                </div>
             </div>
          </div>
          <div class="game-info-container">
             <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn 1</div>
                <div v-if="pointsBoard1 >= pointsBoard2"> + {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
                <div v-else> - {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
             </div>
             <div style="position: relative; display: inline-block; width: 64px; height: 64px;">
                <img :src="getImageUrl('other', 'ResourceIcon')" alt="Resource Icon" class="inline-block h-5 w-5" style="width: 100%; height: 100%; position: relative; z-index: 1;" />
                <span style="position: absolute; font-size: 1.5rem; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 2; color: black;">{{ this.move_request.resources[1] }}</span>
             </div>
          </div>
       </div>
    </div>
    <div v-if="!this.gameEnded" class="mt-[15px] ml-[10%] text-white">
       <input v-model="this.move_request.move" type="text" placeholder="e.g. e2e4" v-on:keyup.enter="makeMove()"
          class="text-black px-4 rounded-[2px] h-[28px] mr-[20px]">
       <button class="bg-[#123456] pl-[15px] pr-[15px] pb-[3px] pt-[3px]" @click="makeMove()">Move</button>
       <div class="text-[#db3d35]">
          {{ this.errorMessage }}
       </div>
    </div>
    <div v-else class="ml-[10%] text-white">
       <button class="bg-[#123456] pl-[15px] pr-[15px] pb-[3px] pt-[3px]" @click="initialize()">Play again</button>
    </div>
 </template>

<script>

import Chessboard from '../components/Chessboard.vue';
import Deployment from '../components/Deployment.vue';
import Decks from '../components/Decks.vue';
import axios from 'axios';
import { baseUrl } from '../base-url.js';

export default {
    components: {
        Deployment,
        Chessboard,
        Decks
    },
    data() {
        return {
            errorMessage: '',
            imageRows: [
                ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant']
            ],
            selectedImageIndex: null,
            boardKey: 0,
            gameEnded: false,
            move_request: {
                move: '',
                turn: 1,
                resources: [],
                board: [[
                [4, 3, 2, 6, 5, 2, 3, 4],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            [
                [4, 3, 2, 6, 5, 2, 3, 4],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]
            ],
            }
        };
    },
    mounted() {
        this.initialize();
    },
    computed: {
        pointsBoard1() {
            return this.calculateBoardPoints(this.move_request.board[1]);
        },
        pointsBoard2() {
            return this.calculateBoardPoints(this.move_request.board[0]);
        }
    },
    methods: {
        initialize() {
            this.gameEnded = false;
            axios.get(`${baseUrl}/initialize`)
                .then(response => {
                    console.log(response.data);
                    this.move_request.board = response.data.board;
                    this.move_request.resources = response.data.resources;
                    this.boardKey++;
                })
                .catch(error => {
                    console.error('Error initializing game:', error);
                });
        },
        getMove(){
            axios.get(`${baseUrl}/move`)
                .then(response => {
                    console.log(response.data);
                    this.move_request.move = response.data.move;
                    this.makeMove();
                })
                .catch(error => {
                    console.error('Error getting move:', error);
                });
        },
        makeMove() {
            this.move_request.board[1].reverse();

            axios.post(`${baseUrl}/move`, this.move_request)
                .then(response => {
                    this.errorMessage = '';
                    this.move_request.move = '';

                    this.gameEnded = response.data.has_game_ended;
                    this.move_request.resources = response.data.resources;
                    this.move_request.board = response.data.playerMoveBoard;
                    this.boardKey++;

                    setTimeout(() => {
                        this.move_request.board = response.data.combinedMoveBoard;
                        this.boardKey++;
                    }, 1000);

                })
                .catch(error => {
                    console.error('Error making move:', error.response.data.detail);
                    this.errorMessage = error.response.data.detail;
                    this.move_request.board[1].reverse();
                });
        },
        handlePositionClicked(position) {
            if (!this.gameEnded) {
                console.log("Position clicked:", position);

            }
        },
        handlePositionConfirmed(position) {
            if (!this.gameEnded) {
                this.move_request.move = position;
                this.makeMove();
            }
        },
        calculatePiecePoints(piece) {
            switch (piece) {
                case 0:
                case 6:
                    return 0;
                case 1:
                    return 1;
                case 2:
                case 3:
                case 8:
                    return 3;
                case 4:
                case 7:
                case 9:
                    return 5;
                case 5:
                    return 9;
                default:
                    return 0;
            }
        },
        calculateBoardPoints(board) {
            let totalPoints = 0;
            for (let row of board) {
                for (let piece of row) {
                    totalPoints += this.calculatePiecePoints(piece);
                }
            }
            return totalPoints;
        },
        getImageUrl(dir, imageName) {
        switch (dir) {
            case 'cards':
                return `/_nuxt/assets/images/cards/${imageName}.png`;
            case 'other':
                return `/_nuxt/assets/images/other/${imageName}.png`;
            default:
                return ''; 
        }
},

        handleImageClick(index) {
            if (this.selectedImageIndex === index) {
                this.selectedImageIndex = null;
            } else {
                this.selectedImageIndex = index;
            }
        },
    }
};


</script>

<style>
body{
    overflow-y: hidden;
}
.cards-container{
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}
.game-info-container{
    position: absolute;
    top: 5%;
    right: 5%;
    display: flex;
}
.selected,
#card:hover {
    border-radius: 5px;
    border-color: rgb(216, 90, 90);
    border-width: 2px;
    border-style: solid;
    height: 163px
}

.background-container {
  position: absolute;
  display: flex;
  justify-content: center;
  z-index: -1;
}

.mirror-image {
  transform: scaleX(-1);
}
</style>