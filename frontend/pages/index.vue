<template>
  <div class="min-h-screen flex flex-col justify-center items-center">
    <div>
      <div id="title-game" class="text-white text-5xl text-center mb-8">
        <img src="https://artofwargame.io/wp-content/uploads/2023/06/Title.png" alt="logo" class="title-image w-20 inline-block" />
      </div>
      <div class="btn-container flex justify-center">
		<a href="/tutorial" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Tutorial</span></p></a>
        <a href="/playplayer" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"><p><span>Player vs. Player</span></p></a>
        <a href="/play" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Player vs. AI</span></p></a>
        <a href="/playAI" class="selectGameBtn text-black px-4 py-2">  <p><span>Ai vs. AI</span></p></a>
      </div>
    </div>
  </div>
</template>

<style>
.title-image {
  position: fixed;
  width: auto;
  height: 50%;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
}

body {
  background-color: #333844;
  font-family: "VoynaFont", sans-serif;
  text-align: center;
  background-image: url("https://artofwargame.io/wp-content/uploads/2023/06/daekroth_parchment_royal_background_brown_4k_714a835b-0a84-4448-ba00-cd3b9ad89f99.jpg");
        background-size: 100% 200%;
        background-repeat: no-repeat;
        background-position: center;
}
.btn-container{
  display: flex;
  flex-direction: column;
}
.selectGameBtn {
	 appearance: none;
	 background: transparent;
	 border: 0;
	 cursor: pointer;
	 filter: drop-shadow(0 0 0.25rem #000 80);
	 transition: all 0.2s ease-in-out;
}
 .selectGameBtn p {
	 aspect-ratio: 8;
	 background: linear-gradient(45deg, #6e4628 0%, #d2b681 50%, #6e4628 100%);
	 border: 0;
	 clip-path: polygon(5% 0%, 95% 0%, 100% 50%, 95% 100%, 5% 100%, 0% 50%);
	 display: block;
	 margin: 0;
	 position: relative;
	 width: 25rem;
}
 .selectGameBtn span {
	 align-items: center;
	 background: radial-gradient(circle, #ca1237 0%, #a60f2d 90%, #820c23 100%);
	 bottom: 0.2rem;
	 box-shadow: inset 0 0 0.5rem 0 rgba(0, 0, 0, 0.5);
	 clip-path: polygon(5% 0%, 95% 0%, 100% 50%, 95% 100%, 5% 100%, 0% 50%);
	 color: #fff;
	 display: flex;
	 font-family: 'Vollkorn SC', 'serif';
	 font-size: 1.2rem;
	 justify-content: center;
	 left: 0.2rem;
	 line-height: 1;
	 margin: 0;
	 position: absolute;
	 right: 0.2rem;
	 text-shadow: 0 0 0.5rem #000;
	 top: 0.2rem;
	 transition: all 0.2s ease-in-out;
}
 .selectGameBtn:hover span {
	 background: radial-gradient(circle, #dc143c 0%, #a60f2d 90%, #820c23 100%);
}
 .selectGameBtn:active span {
	 box-shadow: inset 0 0 1rem 0 #000 80;
	 text-shadow: 0 0 0.25rem #000;
}
</style>