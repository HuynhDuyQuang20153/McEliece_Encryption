
//show model mceliece when click image
const click_show_img = document.getElementById('show');
const click_hide_img = document.getElementById('model_mceliece');

click_show_img.addEventListener('click', function() {
    click_hide_img.classList.add('show'); 
    click_hide_img.style.display = 'block';

});

click_hide_img.addEventListener('click', function() {
    click_hide_img.classList.remove('show'); 
    click_hide_img.style.display = 'none';
});




