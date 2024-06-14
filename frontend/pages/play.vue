<template>
    <div>
        <button class="w-[100px] text-white rounded-full bg-[#5a9679] p-2 m-4" @click="goBack()"><-</button>
    </div>
    <div class="flex w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <aowboard :board="this.move_request.board" :key="boardKey" @position-clicked="handlePositionClicked"
                :isAIGame="false" :cardId="this.selectedImageIndex" ref="aowboard" />
        </div>
        <div class="ml-[50px] flex flex-col w-[40%]">
            <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn {{ this.turn }}</div>
                <div v-if="pointsBoard1 >= pointsBoard2"> + {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
                <div v-else> - {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
            </div>

            <div class="bla ml-[20px] flex flex-row  right-0 ml-auto mb-[12px] text-lg justify-end">
                resource points: {{ this.move_request.resources[1] }}
            </div>
            <div>
                <div v-for="(row, index) in imageRows" :key="index" class="flex flex-row justify-end">
                    <div v-for="(image, imageIndex) in row" :key="imageIndex" class="ml-[10px] ">
                        <img :src="getImageUrl(image)" alt="not working" class="h-[165px] mb-[10px] card"
                            :class="{ 'selected': selectedImageIndex === index + (imageIndex * 3) }" id="card"
                            @click="handleImageClick(index + (imageIndex * 3))" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-if="!this.gameEnded" class="ml-[10%] text-white">
        <input v-model="this.move_request.move" type="text" placeholder="e.g. e2e4" v-on:keyup.enter="makeMove()"
            class="text-black px-4 rounded-[2px] h-[28px] mr-[20px]">
        <button class="bg-[#123456] pl-[15px] pr-[15px] pb-[3px] pt-[3px]" @click="makeMove()">Move</button>
        <div class="text-[#db3d35]">
            {{ this.errorMessage }}
        </div>
    </div>
    <div v-else class="ml-[10%] text-white">
        <button class="bg-[#123456] pl-[15px] pr-[15px] pb-[3px] pt-[3px]" @click="initialize()">Play again</button>
        <div>{{ this.winner }}</div>
    </div>
</template>

<script>
import aowboard from '../components/aowboard.vue';
import axios from 'axios';
import { baseUrl } from '../base-url.js';

export default {
    components: {
        aowboard
    },
    data() {
        return {
            errorMessage: '',
            imageRows: [
                ['hoplite', 'winged knight'],
                ['dutch waterline', 'war elefant']
            ],
            selectedImageIndex: null,
            boardKey: 0,
            gameEnded: false,
            winner: '',
            waterlineCardUsed: false,
            turn: 1,
            move_request: {
                infos: [],
                move: '',
                turn: 1,
                resources: [],
                board: [[
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
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
            this.waterlineCardUsed = false;
            axios.get(`${baseUrl}/initialize`)
                .then(response => {
                    this.move_request.board = response.data.board;
                    this.move_request.resources = response.data.resources;
                    this.boardKey++;
                })
                .catch(error => {
                    console.error('Error initializing game:', error);
                });
        },
        async makeMove() {
            this.move_request.board[1].reverse();

            axios.post(`${baseUrl}/move`, this.move_request)
                .then(response => {
                    this.updateValues(response);
                })
                .catch(error => {
                    console.error('Error making move:', error.response.data.detail);
                    this.errorMessage = error.response.data.detail;
                    this.move_request.board[1].reverse();
                    this.move_request.move = '';
                    this.selectedImageIndex = null;
                });
        },
        updateValues(response) {
            this.errorMessage = '';
            this.move_request.move = '';

            this.infos = response.data.infos;
            this.gameEnded = response.data.has_game_ended;
            this.move_request.resources = response.data.resources;
            this.move_request.board = response.data.playerMoveBoard;
            this.boardKey++;
            this.selectedImageIndex = null;

            if(this.gameEnded) {
                this.checkWinner(this.infos);
            }

            setTimeout(() => {
                this.move_request.board = response.data.combinedMoveBoard;
                this.turn++;
                this.boardKey++;
            }, 1000);
        },
        checkWinner(info) {
            if (info[0][0] == 'check_mate_win') {
                this.winner = 'Black won the game!';
            } else if (info[1][1] == 'check_mate_win') {
                this.winner = 'White won the game!';
            } else {
                this.winner ='The game ended in a draw!';
            }
        },
        handlePositionClicked(position) {
            if (!this.gameEnded) {
                this.checkForWaterlineMove(position);
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
        getImageUrl(imageName) {
            return `/_nuxt/assets/images/cards/${imageName}.png`;
        },
        handleImageClick(index) {
            this.colorSquares();
            if (this.selectedImageIndex === index) {
                this.selectedImageIndex = null;
            } else {
                this.selectedImageIndex = index;
            }
            this.colorWaterlineSquares();
        },
        colorWaterlineSquares() {
            // Color the squares with index 16, 24, 32, 40
            const indexes = [16, 24, 32, 40];
            for (let i = 0; i < indexes.length; i++) {
                if (this.selectedImageIndex === 1 && this.move_request.resources[1] >= 4 && !this.waterlineCardUsed) {
                    document.getElementById(indexes[i]).style.border = '#000 2px solid';
                } else if (this.selectedImageIndex === 1) {
                    document.getElementById(indexes[i]).style.border = '#000 0px solid';
                    this.selectedImageIndex = null;
                }
            }
        },
        checkForWaterlineMove(position) {
            if (position == 'a3h8' || position == 'a6h8' || position == 'a4h8' || position == 'a5h8') {
                this.waterlineCardUsed = true;
            }
        },
        goBack() {
            this.$router.push('/');
        },
        colorSquares() {
            for (let i = 0; i < 64; i++) {
                document.getElementById(i).style.border = '#000 0px solid'
            }
        },
    }
};


</script>

<style>
body {
    background-color: #3B6651;
}

.selected,
#card:hover {
    border-radius: 5px;
    border-color: rgb(216, 90, 90);
    border-width: 2px;
    border-style: solid;
    height: 163px
}
</style>