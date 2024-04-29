<template>
    <div class="flex w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <Chessboard />
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
        <input type="text" placeholder="  e.g. e2e4">
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
            moveInput: 'e2e4',
            turn: 1,
            board: [
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
        };
    },
    mounted() {
        this.makeMove()
    },
    methods: {
        getImageUrl(imageName) {
            return `/_nuxt/assets/images/cards/${imageName}.png`;
        },
        makeMove() {
            axios.post('http://127.0.0.1:8000/move', {
                move: this.moveInput,
                turn: this.turn,
                board: this.board
            })
                .then(response => {
                    console.log('Move response:', response.data);
                })
                .catch(error => {
                    console.error('Error making move:', error);
                });
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
    height: 165px
}
</style>