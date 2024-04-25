<template>
    <div class="flex h-screen w-screen mt-[155px] text-white">
        <div class="ml-[10%] text-2xl">
            <Chessboard />
            <button @click="fetchGameAIvsAI('PPO', 'PPO')">Start AI vs AI</button>
        </div>
        <div class="ml-[50px] flex flex-col w-[40%]">
            <div class="flex flex-row justify-between h-[100px] text-2xl">
                <div>Turn 1</div>
                <div>Your move</div>
            </div>
            <div class="bla ml-[20px] flex flex-row  right-0 ml-auto mb-[12px] text-lg">
                resource points: 0
            </div>
            <div class="bla ml-[20px] flex flex-row  right-0 ml-auto mb-[12px] text-lg">
                k weenie hoe je dat doet, maar hier moeten die grafiekies komen.
            </div>
        </div>
    </div>
</template>

<script>
import Chessboard from '../components/Chessboard.vue';

export default {
  components: {
    Chessboard
  },
  mounted() {
    console.log('Component mounted.')

  },
  methods: {
    async fetchGameAIvsAI(white_model, black_model) {
      const response = await fetch('http://127.0.0.1:8000/aigame', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          white_model: white_model,
          black_model: black_model
        })
      });
      const data = await response.json();
      console.log(data);
    }
  }
};


</script>

<style>
body {
    background-color: #3B6651;
}
</style>