const cardContainer = document.getElementById('card-container');
let translateValue = 0;
let direction = 'right'; // Initial direction of card movement

function moveCards() {
  if (direction === 'left') {
    translateValue -= 200; // Adjust this value based on card width
  } else if (direction === 'right') {
    translateValue += 200; // Adjust this value based on card width
  }

  cardContainer.style.transform = `translateX(${translateValue}px)`;
}

// Automatically move cards every 3 seconds
setInterval(() => {
  moveCards();
}, 3000); // Adjust the interval time as needed