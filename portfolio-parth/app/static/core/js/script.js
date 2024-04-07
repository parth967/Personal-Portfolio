function addFloatingText() {
    const pipeline = document.querySelector('.pipe .body');
    const characters = [];
  
    // Add alphabets (a-z)
    for (let i = 97; i <= 122; i++) {
      characters.push(String.fromCharCode(i));
    }
  
    // Add digits (0-9)
    for (let i = 48; i <= 57; i++) {
      characters.push(String.fromCharCode(i));
    }
  
    // Generate floating text elements
    for (let i = 0; i < 100; i++) { // Adjust the number of characters as needed
      const character = characters[Math.floor(Math.random() * characters.length)];
      const span = document.createElement('span');
      span.textContent = character;
      span.classList.add('floating-text');
      span.style.left = Math.random() * 100 + '%'; // Random horizontal position
      span.style.top = Math.random() * 100 + '%'; // Random vertical position
      pipeline.appendChild(span);
    }
  }
  
  addFloatingText();
  

  document.getElementById('hire-me-btn').addEventListener('click', function() {
    window.location.href = 'mailto:your.email@example.com?subject=Job%20Opportunity&body=Hello,%20I%20am%20interested%20in%20working%20with%20you.%20Please%20contact%20me%20with%20further%20details.';
  });