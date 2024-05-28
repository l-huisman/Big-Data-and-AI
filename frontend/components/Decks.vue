
<template>
    <div class="decks justify-center mr-[100px] w-screen text-white">
         <div class="decks-container opponent" style="top: 0%; display: flex;">
              <div class="deck opponent">
              </div>
              <div class="history opponent">
              </div>
          </div>
          <div class="decks-container playerone" style="top: 0%; display: flex;">
              <div class="deck player">
              </div>
              <div class="history player">
              </div>
          </div>
      </div>
  </template>
  
  
  <script>
  </script>
  
  <style scoped>
  .decks{
      position: absolute;
      width: auto;
      right: 0;
      top: 30%;
  }
  .deck, .history{
      display: flex;
      flex-direction: row;
      background-color: transparent;
      height: 165px;
      width: 110px;
      margin-bottom: 10px;
      margin-left: 20px;
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 1);
      border: 1px solid rgba(0, 0, 0, 0.5);
  }
  </style>
