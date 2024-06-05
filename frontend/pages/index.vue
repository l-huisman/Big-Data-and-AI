
<template>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

  <div class="background-screen min-h-screen flex flex-col justify-center items-center">
    <div>
      <div id="title-game" class="text-white text-5xl text-center mb-8">
        <img src="https://artofwargame.io/wp-content/uploads/2023/06/Title.png" alt="logo" class="title-image w-20 inline-block" />
      </div>
	  <div class="choice-bg">
	</div>

	   <!-- Main Menu Buttons -->
	  <div class="btn-container main flex justify-center">
	    <button class= "selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"  @click="toggleMenus('gamemodes')"> <p><span>Play Game</span></p></button>
		<button class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4" @click="toggleMenus('builddeck')"><p><span>Create Deck</span></p></button>
		<button class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Settings</span></p></button>
	</div>

	    <!-- Game Modes Buttons -->

      <div class="btn-container gamemodes flex justify-center">
		<button class="back-btn" @click="toggleMenus('mainmenu')"><i class="fas fa-chevron-circle-left text-white"></i></button>
		<a href="/tutorial" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Tutorial</span></p></a>
        <a href="/playplayer" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"><p><span>Player vs. Player</span></p></a>
        <a href="/play" class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Player vs. AI</span></p></a>
        <a href="/playAI" class="selectGameBtn text-black px-4 py-2">  <p><span>Ai vs. AI</span></p></a>
	</div>

		   <!-- Deck Builder -->
		<div class = "deck-builder-container">
			<button class="back-btn deckbuilder" style="top: 50px; right: 50px;" @click="toggleMenus('mainmenu')">
			<i class="fas fa-chevron-circle-left text-white"></i>
			</button>
			<div class = "deck-builder-header"></div>
			<div class = "deck-builder-cards">
				<div v-for="(row, index) in imageRows" :key="index" class="flex flex-row justify-end">
					<div v-for="(image, imageIndex) in row" :key="imageIndex" class="ml-[5px] ">
					<img :src="getImageUrl('cards', image)" alt="not working" class="h-[15vw] mb-[10px] deckbuildercard" :class="{ 'selected': selectedImageIndex === index + (imageIndex * 1) }" id="cards" @click="addCardToDeck(index + (imageIndex * 3))"/>
					</div>
				</div>
				<span class="currentPage"> Page {{ currentImageRow }} of 3</span>
				<div class="deck-builder-pagination" style="position: absolute; bottom: -50px; right: 0;">
					<button class="back-btn deckbuilder" style="right: 150px;" @click="nextCards('previous')"><i class="fa fa-chevron-circle-left text-white" aria-hidden="true"></i></button>
					<button class="back-btn deckbuilder" @click="nextCards('next')"><i class="fa fa-chevron-circle-right text-white" aria-hidden="true"></i></button>
				</div>
			</div>
			<div class="deck-builder-items">
				<h2 class="deck-item-count">{{ deckItemsCount }} / 25</h2>
				<div class="deck-builder-button-container">
					<button class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Save Deck</span></p></button>
					<button class="selectGameBtn bg-[#D0C27A] text-black px-4 py-2 mr-4"> <p><span>Import Deck</span></p></button>
				</div>
			</div>

		</div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      errorMessage: '',
      imageRows: [],
      imageRows1: [
        ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant'],
        ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant']
      ],
      imageRows2: [
        ['hoplite', 'hoplite', 'hoplite', 'hoplite', 'dutch waterline', 'war elefant'],
        ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant']
      ],
      imageRows3: [
        ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant'],
        ['hoplite', 'hoplite', 'hoplite', 'winged knight', 'dutch waterline', 'war elefant']
      ],
      selectedImageIndex: null, 
      currentImageRow: 1,
      deckItemsCount: 0 
    };
  },
  created() {
    this.imageRows = JSON.parse(JSON.stringify(this.imageRows1));
  },
  methods: {
    toggleMenus(mode) {
      const choiceBg = document.querySelector('.choice-bg');
      const mainBtns = document.querySelector('.main');
      const gameModes = document.querySelector('.gamemodes');
      const deckBuilder = document.querySelector('.deck-builder-container');
      const deckBuilderCards = document.querySelector('.deck-builder-cards');

      if (gameModes) gameModes.style.bottom = '200%';
      if (mainBtns) mainBtns.style.bottom = '200%';

      switch (mode) {
        case 'mainmenu':
          if (choiceBg) choiceBg.style.opacity = 0;
          if (mainBtns) mainBtns.style.bottom = 'auto';
          if (deckBuilder) deckBuilder.style.bottom = '200%';
          if (deckBuilderCards) deckBuilderCards.style.left = '-200%';
          break;

        case 'gamemodes':
          if (choiceBg) choiceBg.style.opacity = 0.5;
          if (gameModes) gameModes.style.bottom = 'auto';
          break;

        case 'builddeck':
          if (choiceBg) choiceBg.style.opacity = 0;
          if (deckBuilder) deckBuilder.style.bottom = '0';
          if (deckBuilderCards) deckBuilderCards.style.left = '0';
          break;
      }
    },
    getImageUrl(dir, imageName) {
      // Generate URL based on the directory and image name
      switch (dir) {
        case 'cards':
          return `/_nuxt/assets/images/cards/${imageName}.png`;
      }
    },
	nextCards(direction) {
		const deckBuilderCards = document.querySelector('.deck-builder-cards');
		deckBuilderCards.style.left = '-200%';
		
	if (direction === 'next' && this.currentImageRow < 3) {
		this.currentImageRow++;
	} else if (direction === 'previous' && this.currentImageRow > 1) {
		this.currentImageRow--;
	}
	this.imageRows = JSON.parse(JSON.stringify(this['imageRows' + this.currentImageRow]));
		setTimeout(() => {
		deckBuilderCards.style.left = '0'; // Adjust as needed
	}, 500);
	},


    addCardToDeck(index) {
      // Add the card to the deck
      console.log('Card added to deck:', index);
      
      const deckBuilderItems = document.querySelector('.deck-builder-items');
      const deckItemsCount = this.deckItemsCount;
	  const decklimit = 25;

      // Check if a button for this index already exists
      let button = deckBuilderItems.querySelector(`.card-entry-button[data-index='${index}']`);
      if (button) {
        // Get the current count of cards in deck
        let count = parseInt(button.getAttribute('data-count'));
        // Determine the maximum amount of card instances that can be added to the deck. (Kings & Queens = 1, Standard = 4)
        const maxCount = (index == 1 || index == 2) ? 1 : 4;

        if (count < maxCount && deckItemsCount < decklimit) {
          count += 1;
          button.setAttribute('data-count', count);
          button.textContent = `${index} [ x ${count} ]`;
          // Update deckItemsCount
          this.deckItemsCount += 1;
        }
      } else if (deckItemsCount < decklimit){
        // Create a new button if it doesn't exist
        button = document.createElement('button');
        button.className = 'card-entry-button';
        button.setAttribute('data-index', index);
        button.setAttribute('data-count', 1);
        button.textContent = `${index} [ x 1 ]`;
        button.addEventListener('click', this.removeCardFromDeck.bind(this, index));
        deckBuilderItems.appendChild(button);
        // Update deckItemsCount
        this.deckItemsCount += 1;
      }
    },
    removeCardFromDeck(index) {
      const deckBuilderItems = document.querySelector('.deck-builder-items');
      let button = deckBuilderItems.querySelector(`.card-entry-button[data-index='${index}']`);
      if (button) {
        let count = parseInt(button.getAttribute('data-count'));
        if (count > 1) {
          count -= 1;
          button.setAttribute('data-count', count);
          button.textContent = `${index} [ x ${count} ]`;
          // Update deckItemsCount
          this.deckItemsCount -= 1;
        } else {
          deckBuilderItems.removeChild(button);
          // Update deckItemsCount
          this.deckItemsCount -= 1;
        }
      }
    }
  }
};


</script>

<style>

@import url('https://fonts.googleapis.com/css2?family=Almendra:wght@400&display=swap');
.choice-bg{
	position: fixed;
	width: 100vw;
	height: 100vh;
	background-color: black;
	opacity: 0;
	z-index: 500;
	left: 0;
	top: 0;
	transition: 0.5s;
}
.back-btn{
	position: absolute;
	top: 0;
	right: 0;
	transform: scale(3);
}

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
  position: absolute;
  display: flex;
  flex-direction: column;
  z-index: 5000;
  left: 50%;
  transform: translateX(-50%);
}
.gamemodes{
	bottom: 200%;
	transition: 2s;
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
	 font-family: "Almendra", serif;
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

/* STYLING FOR DECK BUILDER */

.deck-builder-container {
  position: fixed;
  width: 100vw;
  height: 100vh;
  background-image: url("https://artofwargame.io/wp-content/uploads/2023/07/daekroth_Background_graphic_medieval_historical_parchment_websi_12404915-1e68-4b92-a5d2-27eaf0686210.jpg");
  background-size: 100% 100%;
  left: 0;
  bottom: 200%;
  transition: 1s;
  z-index: 1000;
}

.background-screen::after, .deck-builder-container::before{
  content: ""; 
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 20px;
  background-image: url("https://artofwargame.io/wp-content/uploads/2023/07/BorderTrimTop.png");
  background-repeat: repeat-x;
  z-index: -1;
}

.deck-builder-container::after, .background-screen::before{
  content: ""; 
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 20px;
  background-image: url("https://artofwargame.io/wp-content/uploads/2023/07/BorderTrimTop.png");
  background-repeat: repeat-x;
  z-index: 2;
}
.deck-builder-cards {
    position: absolute;
    z-index: 50;
    left: -200%;
    top: 50%;
    transform: translateY(-50%);
    padding-left: 5vw;
    transition: 2s;
}

.deck-builder-items {
    position: absolute;
    right: 50px;
    top: 15vh;
    width: 20vw;
    height: 70vh;
    border-left: 2px solid;
}
.deck-item-count{
	position: absolute;
	font-size: 2rem;
	color: white;
	font-family: "Almendra", serif;
	text-transform: uppercase;
  color: white;
  text-shadow: 3px 1px 2px black;
	top: -75px;
}
.currentPage{
	position: absolute;
	font-size: 1.5rem;
	color: white;
	font-family: "Almendra", serif;
	text-transform: uppercase;
	color: white;
	text-shadow: 3px 1px 2px black;
	bottom: -75px;
	left: 75px;

}
.card-entry-button{
	flex-grow: 1;
	width: inherit;
	padding: 10px;
	margin-top: 5px;
	margin-left: 25px;
	border: 1px solid black;
	border-radius: 4px;
	font-size: 16px;
	color: white;
	text-transform: uppercase;
  	text-shadow: 3px 1px 2px black;
	font-family: "Almendra", serif;
	background-image: url(https://artofwargame.io/wp-content/uploads/2023/06/daekroth_Background_graphic_medieval_historical_parchment_websi_170ba6d9-3f9a-4f7a-b464-cccdc4d66e00.jpg);
	background-repeat: no-repeat;
	background-size: cover;
}
.deckbuildercard:hover {
    box-shadow: 0 0 10px rgba(21, 255, 0, 1);
	scale: 1.25;
}
.deck-builder-button-container{
	position: absolute;
	bottom: -70px;
}
</style>