/* Script adds movements to the header */

/* Logo appearence effect */
logo = document.querySelector('.title__logo')
under_logo = document.querySelector('.under__title')

setTimeout(() => {
   logo.classList.add('_active');
}, 300);
setTimeout(() => {
   under_logo.classList.add('_active');
}, 500);
setTimeout(() => {
   logo.style.transition = 'all 0.01s ease 0s'
   under_logo.style.transition = 'all 0.01s ease 0s'
}, 500);


/* Parallax effect for title and logo in the header. */
logo = document.querySelector('.title__logo');
under = document.querySelector('.under__title');

function parallax(event) {
   logo.style.transform = 'translate(-' + event.clientX / 80 + 'px, -' + event.clientY / 80 + 'px)'
   under.style.transform = 'translate(-' + event.clientX / 50 + 'px, -' + event.clientY / 70 + 'px)'
};

document.querySelectorAll('.parallax').forEach(item => {
   item.addEventListener('mousemove', parallax);
});
