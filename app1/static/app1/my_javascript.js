//c:/Users/xario/PycharmProjects/django_app/venv/Scripts/Activate.ps1 ;  cd haider_site;  python manage.py runserver
var mediaQuery320_400 = window.innerWidth >= 320 && window.innerWidth < 400;
var mediaQuery400_600 = window.innerWidth >= 400 && window.innerWidth < 600;
var mediaQuery600_800 = window.innerWidth >= 600 && window.innerWidth < 800;

var mediaQuery800_1000 = window.innerWidth >= 800 && window.innerWidth < 1000;
var mediaQuery1000_1100= window.innerWidth >= 1000  && window.innerWidth < 1100;
var mediaQuery1100_1300 = window.innerWidth >= 1100  && window.innerWidth < 1300;
var mediaQuery1300_ = window.innerWidth >= 1300;

var allMediaQueries = [mediaQuery320_400, mediaQuery400_600, mediaQuery600_800, 
                       mediaQuery800_1000, mediaQuery1000_1100, mediaQuery1100_1300, 
                       mediaQuery1300_];

let footer = document.querySelector('.footer');
footer.style.top = (window.screen.height) + "px";

var window_media_query_offset = 17;

let container = document.querySelector("body");
console.log("this is main JS");

new ResizeSensor(container, function()
{
    // console.log("dimension changed:", container.clientWidth, container.clientHeight);
    let footer = document.querySelector('.footer');
    if (footer) {
    footer.style.top = (container.clientHeight)*1 + "px";
    // footer.style.top = (window.screen.height - footer.offsetHeight)*0.72  + "px";
    }
});
// horizental-resizer


// utility
function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i] === obj) {
            return true;
        }
    }
    return false;
}



//drop_menu_list   document.querySelectorAll('.profile-pic-wrap *');
document.body.addEventListener("click", function(event) {
    
    
    let x = document.querySelectorAll('.profile-pic-wrap *');
    let nodeList = Array.from(x);
    let x2 = document.querySelectorAll('.drop_menu *');
    let nodeList2 = Array.from(x2);
    nodeList = nodeList.concat(nodeList2);
    let y = event.target;
    let check = nodeList.includes(y);

    

    if (check) {
       


        // drop_down_function();
        // profile_drop_down_function();

    } else {
        

        let drop_ml = document.querySelector("#drop_menu_list");
        let drop_prof = document.querySelector('.profile-drop-menu');
        let hammies = document.querySelectorAll('.hamburger_button_inner');

        if (drop_prof.style.maxHeight != "0px" && drop_prof.style.maxHeight != "") {
            console.log(" drop menu is shown");
            drop_prof.style.maxHeight = "0";
            drop_prof.style.transition = 'none';
            drop_prof.style.border = '0px ridge white';
            drop_prof.style.boxShadow = 'none';

        } else {
            
        }


        if (drop_ml.style.maxHeight != "0px" && drop_ml.style.maxHeight != "") {
            console.log(" drop menu ml is shown");
            drop_ml.style.maxHeight = "0";
            drop_ml.style.transition = 'none';
            drop_ml.style.border = '0px ridge white';
            drop_ml.style.boxShadow = 'none';
            hammies.forEach(elem => elem.classList.toggle("change"));

        } else {
           
        }

    }
});




function drop_down_function() {

    var x = document.querySelector("#drop_menu_list");
    var hammies = document.querySelectorAll('.hamburger_button_inner');


    if (x.style.maxHeight == "0" || x.style.maxHeight === 0 ||
        x.style.maxHeight == "0px" || x.style.maxHeight == "") {

       

        x.style.opacity = '1';
        x.style.maxHeight = "300px";
        x.style.border = '1px ridge #686de0';
        x.style.boxShadow = '3px 5px 10px 5px #88888842';
        x.style.transition = 'max-height 0.3s ease-in, border 0.3s ease-out, box-shadow 0.3s ease-out';
        hammies.forEach(elem => elem.classList.toggle("change"))


    } else {

       

        x.style.maxHeight = "0";
        x.style.transition = 'none';
        x.style.border = '0px ridge white';
        x.style.boxShadow = 'none';
        hammies.forEach(elem => elem.classList.toggle("change"))
    }

}

//profile-drop-menu

function profile_drop_down_function() {

    var x = document.querySelector(".profile-drop-menu");



    if (x.style.maxHeight == "0" || x.style.maxHeight === 0 ||
        x.style.maxHeight == "0px" || x.style.maxHeight == "") {

       

        x.style.opacity = '1';
        x.style.maxHeight = "400px";
        x.style.border = '1px ridge #686de0';
        x.style.boxShadow = '3px 5px 10px 5px #88888842';
        x.style.transition = 'max-height 0.3s ease-in, border 0.3s ease-out, box-shadow 0.3s ease-out';


    } else {


        x.style.maxHeight = "0";
        x.style.transition = 'none';
        x.style.border = '0px ridge white';
        x.style.boxShadow = 'none';

    }

}


function show_profile_edit(element) {

    // click happens on user-name-item   or email-item element
    console.log(' ------->>>>> ', element);

    let clist = Array.from(element.classList);
    
    if(clist.includes('user-name-item')) {

        var e = document.getElementById("user-name-prompt").classList;
        e.add('hidden');
        if (Array.from(e).includes('shown')) {
            e.remove('shown');
        }

        var c = document.getElementById("user-update-field").classList;
        c.add('shown');
        if (Array.from(c).includes('hidden')) {
            c.remove('hidden');
        }
    }
    else if (clist.includes('email-item')) {

        var e = document.getElementById("email-prompt").classList;
        e.toggle('hidden');
        var c = document.getElementById("email-update-field").classList;
        c.toggle('shown');
    }
    
}


// function on finishing updating and clicking 'Update'
function update_profile_info(element) {    
    console.log(' ------->>>>> ', element);

    let clist = Array.from(element.classList);
    
    if(clist.includes('user-update-btn')) {
        console.log('yee');
        var e = document.getElementById("user-name-prompt").classList;
        e.add('shown');
        if (Array.from(e).includes('hidden')) {
            e.remove('hidden');
        }

        var c = document.getElementById("user-update-field").classList;
        c.add('hidden');
        if (Array.from(c).includes('shown')) {
            c.remove('shown');
        }
    }

    else if (clist.includes('email-update-btn')) {

        var e = document.getElementById("email-prompt").classList;
        e.toggle('shown');
        var c = document.getElementById("email-update-field").classList;
        c.toggle('hidden');
    }


}


function spawnWelcomeText() {

    setTimeout( function() {
        let e = document.querySelector(".welcome-text");
        e.style.opacity = "1";
    }
        , 500);
}


function navigateToUrl(elementClicked) {
    let url = elementClicked.getAttribute('data-url');
    window.open(
        url,
        '_blank' // <- This is what makes it open in a new window.
      );
}



spawnWelcomeText();




// 


// me:  tHIS Code removes the browser message when we referesh the form page
// if ( window.history.replaceState ) {
//     window.history.replaceState( null, null, window.location.href );
//   }