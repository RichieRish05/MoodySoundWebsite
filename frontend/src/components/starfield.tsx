import React, { useRef, useEffect } from 'react';

function Starfield() {
  const canvasRef = useRef(null);
  const starsRef = useRef([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Resize the canvas to fill the browser window
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // initial sizing

    // Configuration
    const STAR_COUNT = 200;        // Number of stars
    const STAR_COLOR = '#ffffff';  // Star color (white)
    const STAR_SIZE = 2;          // Radius of each star
    const STAR_SPEED = 0.7;       // Speed factor for vertical movement

    // Initialize star positions
    starsRef.current = [];
    for (let i = 0; i < STAR_COUNT; i++) {
      starsRef.current.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        speed: (Math.random() - 0.5) * STAR_SPEED, // random speed variation
      });
    }

    // Function to draw a single star
    const drawStar = (x, y, radius) => {
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2, false);
      ctx.fillStyle = STAR_COLOR;
      ctx.fill();
    };

    // Animation loop
    const animate = () => {
      // Clear the canvas each frame
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update and draw each star
      for (let i = 0; i < starsRef.current.length; i++) {
        const star = starsRef.current[i];
        // Move the star downward
        star.y += star.speed;
        // If the star goes off-screen, reset it to the top
        if (star.y > canvas.height) {
          star.y = -STAR_SIZE;
          star.x = Math.random() * canvas.width;
        }
        // Draw the star
        drawStar(star.x, star.y, STAR_SIZE);
      }

      requestAnimationFrame(animate);
    };

    // Start the animation
    animate();

    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);

  // Inline styles to fill the screen and have a black background
  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        zIndex: 0
      }}

    />
  );
}

export default Starfield;
