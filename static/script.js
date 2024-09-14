// Add event listener to the form submit button
document.querySelector('button[type="submit"]').addEventListener('click', (e) => {
    e.preventDefault();
    const fullname = document.querySelector('input[name="fullname"]');
    const phonenumber = document.querySelector('input[name="phonenumber"]');
    const email = document.querySelector('input[name="email"]');
    const message = document.querySelector('textarea[name="message"]');
  
    if (!fullname.value || !phonenumber.value || !email.value || !message.value) {
      alert('Please fill out all fields');
      return;
    }
  
    // Add animation to the form submission
    document.querySelector('form').classList.add('animate-submit');
  
    // Simulate a form submission delay
    setTimeout(() => {
      alert(`Thank you for your message, ${fullname.value}!`);
      document.querySelector('form').reset();
      document.querySelector('form').classList.remove('animate-submit');
    }, 2000);
  });
  
  // Add animation to the icons on hover
  document.querySelectorAll('.icons-social a').forEach((icon) => {
    // Add your animation code here
    icon.addEventListener('mouseover', () => {
      icon.classList.add('animate-icon');
    });
    icon.addEventListener('mouseout', () => {
      icon.classList.remove('animate-icon');
    });
  });