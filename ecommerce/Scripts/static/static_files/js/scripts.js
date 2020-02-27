
function scroll_to(clicked_link, nav_height) {
	var element_class = clicked_link.attr('href').replace('#', '.');
	var scroll_to = 0;
	if(element_class != '.top-content') {
		element_class += '-container';
		scroll_to = $(element_class).offset().top - nav_height;
	}
	if($(window).scrollTop() != scroll_to) {
		$('html, body').stop().animate({scrollTop: scroll_to}, 1000);
	}
}


jQuery(document).ready(function() {
	
	/*
	    Navigation
	*/
	$('a.scroll-link').on('click', function(e) {
		e.preventDefault();
		scroll_to($(this), $('nav').outerHeight());
	});
	// toggle "navbar-no-bg" class
	$('.top-content .text').waypoint(function() {
		$('nav').toggleClass('navbar-no-bg');
	});
	
   

    /*
	    Search form
	*/
	$('.navbar-search-button .search-button').on('click', function(e){
		e.preventDefault();
		$(this).blur();

		$('.navbar-menu-items').toggleClass('disabled fadeIn animated');
		$('.navbar-search-form').toggleClass('disabled fadeInLeft animated');
		$('.navbar-search-form input.search').val('').focus();
	});


});

function isNumber(event){
  	var keycode=event.keyCode;
  	if(keycode > 47 && keycode < 58){
  		return true;
  	}
  	return false;
  }
function myFunction() {
  
document.getElementById("categoryname").value=document.getElementById("on-change").innerHTML
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */


function category() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("li");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].innerHTML;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}
function getPaging(text) {
  document.getElementById("myInput").value=text.innerHTML;
}

