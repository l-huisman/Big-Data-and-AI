<template>
    <div class="flex w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <Chessboard :board="this.move_request.board" :key="boardKey" />
        </div>
        <div class="ml-[50px] flex flex-col w-[40%]">
            <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn 1</div>
                <div v-if="pointsBoard1 >= pointsBoard2"> + {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
                <div v-else> - {{ Math.abs(pointsBoard1 - pointsBoard2) }}</div>
            </div>
            <div class="bla ml-[20px] flex flex-row  right-0 ml-auto mb-[12px] text-lg justify-end">
                resource points: 0
            </div>
            <div>
                <div v-for="(row, index) in imageRows" :key="index" class="flex flex-row justify-end">
                    <div v-for="(image, imageIndex) in row" :key="imageIndex" class="ml-[10px] ">
                        <img :src="getImageUrl(image)" alt="not working" class="h-[165px] mb-[10px]" id="card" />
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="ml-[10%] text-white">
        <input v-model="this.move_request.move" type="text" placeholder="e.g. e2e4"
            class="text-black px-4 rounded-[2px] h-[28px] mr-[20px]">
        <button class="bg-[#123456] pl-[15px] pr-[15px] pb-[3px] pt-[3px]" @click="makeMove()">Move</button>
        <div class="text-[#db3d35]">
            {{ this.errorMessage }}
        </div>
    </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';
import axios from 'axios';

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
            boardKey: 0,
            recoursePoints: 0,
            temporaryBoard: [],
            move_request: {
                move: '',
                turn: 1,
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
    computed: {
        pointsBoard1() {
            return this.calculateBoardPoints(this.move_request.board[1]);
        },
        pointsBoard2() {
            return this.calculateBoardPoints(this.move_request.board[0]);
        }
    },
    methods: {
        getImageUrl(imageName) {
            return `/_nuxt/assets/images/cards/${imageName}.png`;
        },
        makeMove() {
            this.move_request.board[0].reverse();

            axios.post('http://127.0.0.1:8000/move', this.move_request)
                .then(response => {
                    this.errorMessage = '';
                    this.recoursePoints += 1;
                    this.move_request.move = '';

                    this.move_request.board[1] = response.data.board[1];
                    this.boardKey++;

                    setTimeout(() => {
                        this.move_request.board[0] = response.data.board[0];
                        this.boardKey++;
                    }, 2000);
                })
                .catch(error => {
                    console.error('Error making move:', error.response.data.detail);
                    this.errorMessage = error.response.data.detail;
                    this.move_request.board[0].reverse();
                });
        },
        calculatePiecePoints(piece) {
            switch (piece) {
                case 0:
                    return 0; // Empty square
                case 1:
                    return 1; // Pawn
                case 2:
                    return 3; // Bishop
                case 3:
                    return 3; // Knight
                case 4:
                    return 5; // Rook
                case 5:
                    return 9; // Queen
                case 6:
                    return 5; // Winged Knight
                case 7:
                    return 3; // Hoplite
                case 8:
                    return 5; // War Elephant
                case 9:
                    return 0; // King
                default:
                    return 0; // Handle unknown pieces
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
        }
    }
};


</script>

<style>
body {
    background-color: #3B6651;
}

#card:hover {
    border-radius: 5px;
    border-color: rgb(216, 90, 90);
    border-width: 2px;
    border-style: solid;
    height: 163px
}
</style>