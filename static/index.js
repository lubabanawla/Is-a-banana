const banana = document.getElementById('banana');
const bobbuddy = document.getElementById('bobbuddy');
const speechBubble = document.getElementById('speech-bubble');
const speechText = document.getElementById('speech-text');
const actionButton = document.getElementById('action-button');

let x = 0;
let y = 0;
let dx = 2;
let dy = 2;
let imageIndex = 0;
const images = ['bananaimage1.png', 'bananaimage2.png', 'bananaimage3.png'];

function animate() {
  const maxX = window.innerWidth - banana.width;
  const maxY = window.innerHeight - banana.height;

  x += dx;
  y += dy;

  if (x < 0 || x > maxX) {
    dx = -dx;
    changeBananaImage();
  }
  if (y < 0 || y > maxY) {
    dy = -dy;
    changeBananaImage();
  }

  banana.style.left = x + 'px';
  banana.style.top = y + 'px';

  requestAnimationFrame(animate);
}

function changeBananaImage() {
  imageIndex = (imageIndex + 1) % images.length;
  banana.src = staticBaseUrl + images[imageIndex];
}

animate();

// Minion Buddy functionality
const minionPhrases = [
  "Bello!",
  "Banana!",
  "Poopaye!",
  "Tank yu!",
  "Tulaliloo ti amo!",
];

function showRandomPhrase() {
  const randomPhrase = minionPhrases[Math.floor(Math.random() * minionPhrases.length)];
  speechText.textContent = randomPhrase;
  speechBubble.classList.remove('hidden');
  setTimeout(() => {
    speechBubble.classList.add('hidden');
  }, 3000);
}

function showMultiplyButton() {
  actionButton.textContent = "CLICK ME! CLICK ME! CLICK ME!";
  actionButton.classList.remove('hidden');
  actionButton.onclick = multiplyMinions;
}

function multiplyMinions() {
  const minions = [];
  const minionSpeed = 2;
  
  // Create 100 minions
  for (let i = 0; i < 100; i++) {
    const newMinion = document.createElement('img');
    newMinion.src = staticBaseUrl + 'minionmultiplier.png';
    newMinion.className = 'moving-minion';
    newMinion.style.position = 'absolute';
    newMinion.style.width = '50px';
    newMinion.style.height = '50px';
    newMinion.style.left = Math.random() * (window.innerWidth - 50) + 'px';
    newMinion.style.top = Math.random() * (window.innerHeight - 50) + 'px';
    newMinion.style.cursor = 'pointer';
    
    // Add random movement direction
    const dx = (Math.random() - 0.5) * minionSpeed * 2;
    const dy = (Math.random() - 0.5) * minionSpeed * 2;
    
    // Store movement parameters on the element itself
    newMinion.dataset.dx = dx;
    newMinion.dataset.dy = dy;
    
    // Click handler to remove minion
    newMinion.onclick = function() {
      this.remove();
      minions.splice(minions.indexOf(this), 1);
      updateMinionCounter();
    };
    
    document.body.appendChild(newMinion);
    minions.push(newMinion);
  }

  // Add counter display
  const counter = document.createElement('div');
  counter.id = 'minion-counter';
  counter.textContent = `Minions remaining: ${minions.length}`;
  counter.style.position = 'fixed';
  counter.style.top = '10px';
  counter.style.right = '10px';
  counter.style.color = 'white';
  counter.style.zIndex = '1000';
  document.body.appendChild(counter);

  // Animation loop
  function animateMinions() {
    minions.forEach(minion => {
      let x = parseFloat(minion.style.left) || 0;
      let y = parseFloat(minion.style.top) || 0;
      let dx = parseFloat(minion.dataset.dx);
      let dy = parseFloat(minion.dataset.dy);

      // Update position
      x += dx;
      y += dy;

      // Bounce off walls
      if (x < 0 || x > window.innerWidth - 50) {
        dx = -dx;
        minion.dataset.dx = dx;
      }
      if (y < 0 || y > window.innerHeight - 50) {
        dy = -dy;
        minion.dataset.dy = dy;
      }

      minion.style.left = x + 'px';
      minion.style.top = y + 'px';
    });

    if (minions.length > 0) {
      requestAnimationFrame(animateMinions);
    }
  }

  function updateMinionCounter() {
    counter.textContent = `Minions remaining: ${minions.length}`;
    if (minions.length === 0) {
      counter.textContent = 'ALL MINIONS VANQUISHED!';
      setTimeout(() => counter.remove(), 2000);
    }
  }

  animateMinions();
  actionButton.classList.add('hidden');
}

function performRandomAction() {
  const randomAction = Math.random();
  if (randomAction < 0.7) {
    showRandomPhrase();
  } else {
    showMultiplyButton();
  }
}

setInterval(performRandomAction, 10000); // Perform a random action every 10 seconds
