//reload page
function reloadPage() {
    location.reload();
}

//toggle icon navbar (show menu khi chon icon 3 gach)
// let menuIcon = document.querySelector('#menu-icon');
// let navbar = document.querySelector('.navbar');

// menuIcon.onclick = () => {
//     menuIcon.classList.toggle('bx-x');
//     navbar.classList.toggle('active');
// }

//scroll section
let sections = document.querySelectorAll('section');
let navlinks = document.querySelectorAll('header nav a');

window.onscroll = () =>{
    //sticky header
    let header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 100); //khi luot man hinh xuong 100px thi se them class sticky vao header


    //thay doi active khi chon tung menu
    sections.forEach(sec =>{
        let top = window.scrollY;
        let offset = sec.offsetTop - 100;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if(top > offset && top < offset + height){
            navlinks.forEach(links =>{
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });

            //activie section for animatin on scroll
            sec.classList.add('show-animate');
        }
        //if want to use animation that repeats on scroll use this
        else{
            sec.classList.remove('show-animate');
        }
    });


    //tat menu khi scroll
    // menuIcon.classList.remove('bx-x');
    // navbar.classList.remove('active');

    //add class 'animation' in footer when scroll
    let footer =  document.querySelector('footer');
    footer.classList.toggle('show-animate', this.innerHeight + this.scrollY >= document.scrollingElement.scrollHeight);

    //tat model mceliece khi scroll
    click_hide_img.classList.remove('show'); 
    click_hide_img.style.display = 'none';
    hide_bg.style.display = 'none';
}

//show model mceliece when click image
const click_show_img = document.getElementById('show');
const click_hide_img = document.getElementById('model_mceliece');
const hide_bg = document.getElementById('hide-bg');

click_show_img.addEventListener('click', function() {
    click_hide_img.classList.add('show'); 
    click_hide_img.style.display = 'block';
    hide_bg.style.display = 'block';

});

click_hide_img.addEventListener('click', function() {
    click_hide_img.classList.remove('show'); 
    click_hide_img.style.display = 'none';
    hide_bg.style.display = 'none';
});




