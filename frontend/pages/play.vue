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
            <div class="bla ml-[20px] flex flex-row  right-0 ml-auto mb-[12px] text-lg">
                resource points: 0
            </div>
            <div>
                <div v-for="(row, index) in imageRows" :key="index" class="flex flex-row ">
                    <div v-for="(image, imageIndex) in row" :key="imageIndex" class="mr-[10px] w-fit right-0 ml-auto">
                        <img :src="getImageUrl(image)" alt="not working" class="h-[165px] mb-[10px]" />
                    </div>
                </div>
                <!-- <div class=" flex flex-row">
                    <img src="../assets/images/cards/hoplite.png" alt="not working"
                        class=" h-[180px] mr-[10px] right-0 ml-auto mb-[20px]">
                    <img src="../assets/images/cards/hoplite.png" alt="not working" class=" h-[180px] mr-[10px]">
                    <img src="../assets/images/cards/hoplite.png" alt="not working" class=" h-[180px]">
                </div>
                <div class=" flex flex-row">
                    <img src="../assets/images/cards/winged knight.png" alt="not working"
                        class=" h-[180px] mr-[10px] right-0 ml-auto mb-[20px]">
                    <img src="../assets/images/cards/dutch waterline.png" alt="not working" class=" h-[180px] mr-[10px]">
                    <img src="../assets/images/cards/war elefant.png" alt="not working" class=" h-[180px]">
                </div> -->
            </div>
        </div>
    </div>

    <div class="ml-[10%] text-white">
        <!-- <div>e.g. e2e4</div> -->
        <input type="text" placeholder="  e.g. e2e4">
    </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';

export default {
  components: {
    Chessboard
  },
  data() {
    return {
      imageRows: [
        ['hoplite', 'hoplite', 'hoplite'],
        ['winged knight', 'dutch waterline', 'war elefant']
      ]
    };
  },
  methods: {
    getImageUrl(imageName) {
        return `/_nuxt/assets/images/cards/${imageName}.png`;
    }
  }
};


</script>

<style>
body {
    background-color: #3B6651;
}
</style>