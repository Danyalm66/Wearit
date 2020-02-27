
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
  	if(keycode>48 && keycode<57){
  		return true;
  	}
  	return false;
  }