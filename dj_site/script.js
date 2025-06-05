document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    document.getElementById('status').innerText = 'Thanks, we will get back to you soon!';
    this.reset();
});
