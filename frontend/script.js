const canvas = document.getElementById("video-canvas");
const context = canvas.getContext("2d");

const frameCount = 300;
const currentFrame = index => (
  `ezgif-81dd60d601a10340-jpg/ezgif-frame-${index.toString().padStart(3, '0')}.jpg`
);

const images = [];
let framesLoaded = 0;

// Setup canvas size
canvas.width = 1920;
canvas.height = 1080;

// Preload images
for (let i = 1; i <= frameCount; i++) {
  const img = new Image();
  img.src = currentFrame(i);
  img.onload = () => {
    framesLoaded++;
    if (framesLoaded === 1) {
      // Draw first frame as soon as it loads
      render(0);
    }
  };
  images.push(img);
}

// State for scrolling and easing
let scrollProgress = 0; // Target frame index (0 to frameCount - 1)
let currentDrawnFrame = 0; // The actual frame being drawn (eased)

// Navbar scroll effect
const navbar = document.getElementById("navbar");

window.addEventListener("scroll", () => {
  // Update navbar
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }

  // Calculate scroll progress for the canvas
  const scrollTop = document.documentElement.scrollTop;
  const maxScrollTop = document.documentElement.scrollHeight - window.innerHeight;
  const scrollFraction = scrollTop / maxScrollTop;
  
  // Update target frame
  scrollProgress = scrollFraction * (frameCount - 1);
  
  // Manage text overlays based on scroll fraction
  updateTextOverlays(scrollFraction);

  // Redirect to dashboard at the end of the scroll
  if (scrollFraction > 0.99 && !window.isRedirecting) {
      window.isRedirecting = true;
      document.body.style.transition = "opacity 0.8s ease";
      document.body.style.opacity = "0";
      setTimeout(() => {
          window.location.href = "index.html";
      }, 800);
  }
});

function updateTextOverlays(fraction) {
    const step1 = document.querySelector('.step-1');
    const step2 = document.querySelector('.step-2');
    const step3 = document.querySelector('.step-3');
    
    // Step 1: ~15% to 35%
    step1.classList.toggle('visible', fraction > 0.15 && fraction < 0.35);
    // Step 2: ~45% to 65%
    step2.classList.toggle('visible', fraction > 0.45 && fraction < 0.65);
    // Step 3: ~75% to 95%
    step3.classList.toggle('visible', fraction > 0.75 && fraction < 0.95);
}

function render(frameIndex) {
  if (images[frameIndex] && images[frameIndex].complete) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    // Draw image covering the canvas (if aspect ratios differ, adjust here, but usually drawing full size is fine if canvas object-fit is cover)
    context.drawImage(images[frameIndex], 0, 0, canvas.width, canvas.height);
  }
}

// Animation loop to ease the frame drawing
function loop() {
  // Lerp between current drawn frame and target frame (scrollProgress)
  // 0.1 is the easing factor (closer to 1 = faster, closer to 0 = smoother/slower)
  currentDrawnFrame += (scrollProgress - currentDrawnFrame) * 0.1;
  
  const frameToDraw = Math.min(
    frameCount - 1,
    Math.max(0, Math.floor(currentDrawnFrame))
  );
  
  render(frameToDraw);
  
  requestAnimationFrame(loop);
}

// Start loop
loop();

// Handle resize to keep canvas responsive
window.addEventListener("resize", () => {
    // If needed, we can adjust canvas width/height to match window exactly,
    // but object-fit: cover in CSS handles the scaling gracefully.
});
