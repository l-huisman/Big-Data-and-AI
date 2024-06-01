<template>
    <div class="flex w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <Chessboard :board="this.move_request.board" :key="boardKey" @position-clicked="handlePositionClicked"
                :isAIGame="false" ref="aowboard" />
        </div>
        <div class="ml-[50px] flex flex-col w-[40%]">
            <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn 1</div>
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
    </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';
import axios from 'axios';
import { baseUrl } from '../base-url.js';

export default {
    components: {
        Chessboard
    },
    data() {
        return {
            errorMessage: '',
            imageRows: [
                ['hoplite', 'hoplite', 'hoplite'],
                ['winged knight', 'dutch waterline', 'war elefant']
            ],
            selectedImageIndex: null,
            boardKey: 0,
            gameEnded: false,
            move_request: {
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
        async makeMove() {
            this.move_request.board[1].reverse();

            // check for possible moves
            let possibleMoves = await this.calculatePossibleMoves(this.move_request.move);
            console.log(possibleMoves);
            let transformedPos = this.move_request.move.charAt(0) + (9 - parseInt(this.move_request.move.charAt(1))).toString() + this.move_request.move.charAt(2) + (9 - parseInt(this.move_request.move.charAt(3))).toString();

            if (!possibleMoves.includes(transformedPos)) {
                console.log('Invalid move')
                this.move_request.move = 'e2e4';
                return;
            }

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
                    console.log(this.move_request.move)
                    this.errorMessage = error.response.data.detail;
                    this.move_request.board[1].reverse();
                    this.move_request.move = '';
                });
        },
        async calculatePossibleMoves(move) {
            let position = move.charAt(0) + move.charAt(1);
            position = position.charAt(0) + (9 - parseInt(position.charAt(1))).toString();
            console.log(position);
            const response = await fetch(`${baseUrl}/actions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    board: [this.gameBoard],
                    turn: 1,
                    pieceLocation: position
                })
            });
            const data = await response.json();
            console.log(data);
            return data.possibleMoves;
        },
        handlePositionClicked(position) {
            if (!this.gameEnded) {
                if (position.length == 4) {
                    this.move_request.move = position;
                    this.makeMove();
                }
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