<template>
    <div class="flex w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <Chessboard :board="this.move_request.board" :key="boardKey" />
        </div>
        <div class="ml-[50px] flex flex-col w-[40%]">
            <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn 1</div>
                <div>Your move</div>
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
            imageRows: [
                ['hoplite', 'hoplite', 'hoplite'],
                ['winged knight', 'dutch waterline', 'war elefant']
            ],
            boardKey: 0,
            recoursePoints: 0,
            temporaryBoard: [],
            move_request: {
                move: 'e2e4',
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
    methods: {
        getImageUrl(imageName) {
            return `/_nuxt/assets/images/cards/${imageName}.png`;
        },
        parseMove(move) {
            const fileFrom = move.charCodeAt(0) - 'a'.charCodeAt(0);
            const rankFrom = parseInt(move[1]) - 1;
            const fileTo = move.charCodeAt(2) - 'a'.charCodeAt(0);
            const rankTo = parseInt(move[3]) - 1;
            return { fileFrom, rankFrom, fileTo, rankTo };
        },
        applyMove(move) {
            const { fileFrom, rankFrom, fileTo, rankTo } = this.parseMove(move);
            const piece = this.move_request.board[1][rankFrom][fileFrom];
            this.move_request.board[1][rankTo][fileTo] = piece;
            this.move_request.board[1][rankFrom][fileFrom] = 0;
        },
        undoMove(move) {
            const { fileFrom, rankFrom, fileTo, rankTo } = this.parseMove(move);
            const piece = this.move_request.board[1][rankTo][fileTo];
            this.move_request.board[1][rankFrom][fileFrom] = piece; 
            this.move_request.board[1][rankTo][fileTo] = 0; 
        },
        makeMove() {
            this.applyMove(this.move_request.move)
            this.boardKey++;
            this.move_request.board[0].reverse();

            setTimeout(() => {
                this.undoMove(this.move_request.move)
                this.move_request.board[0].reverse();
                console.log(this.move_request.board)

                axios.post('http://127.0.0.1:8000/move', this.move_request)
                    .then(response => {
                        this.move_request.board = response.data.board;
                        // this.move_request.turn += 1;
                        this.recoursePoints += 1;
                        this.move_request.move = '';
                        this.boardKey++;
                    })
                    .catch(error => {
                        console.error('Error making move:', error.response.data.detail);
                    });
            }, 2000);
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