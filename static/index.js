const banana = document.getElementById('banana');
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
