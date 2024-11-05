/* responsive menu */
function openNav() {
    $('body').addClass("active");
    document.getElementById("mySidenav").style.width = "280px";
}
function closeNav() {
    $('body').removeClass("active");
    document.getElementById("mySidenav").style.width = "0";
}

 /* loader */
$(window).load(function myFunction() {
  $(".s-panel .loader").removeClass("wrloader");
});

//go to top
$(document).ready(function () {
    $("#common-home").parent().addClass("home-page");
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('#scroll').fadeIn();
        } else {
            $('#scroll').fadeOut();
        }
    });
    $('#scroll').click(function () {
        $("html, body").animate({scrollTop: 0}, 600);
        return false;
    });
});


$(document).ready(function () {
    if ($(window).width() <= 991) {
        $('.menusp').appendTo('.appmenu');
        $('.curr').appendTo('.haccount');
        $('.langg').appendTo('.haccount');
        
        $('.serchapp').appendTo('.appendsearch');
    }

    $('.toprightw .owl-carousel.owl-theme .owl-buttons').appendTo('.apponbtn');

});


function openSearch() {
    $('body').addClass("active-search");
    document.getElementById("search").style.height = "auto";
    $('#search').addClass("sideb");
    // $('.search_query').attr('autofocus', 'autofocus').focus();
}
function closeSearch() {
    $('body').removeClass("active-search");
    document.getElementById("search").style.height = "0";
    $('#search').addClass("siden");
    // $('.search_query').attr('autofocus', 'autofocus').focus();
}


$(document).ready(function () {
$("#ratep,#ratecount").click(function() {
    $('body,html').animate({
        scrollTop: $(".product-tab").offset().top 
    }, 1500);
});
});

/* dropdown effect of account */
$(document).ready(function () {
    if ($(window).width() <= 767) {
    $('.catfilter').appendTo('.appres');

    $('.dropdown a.account').on("click", function(e) {
        $(this).next('ul').toggle();
        e.stopPropagation();
        e.preventDefault();
    });
}
});

$(document).ready(function () {
$('.dropdown button.test').on("click", function(e)  {
    $(this).next('ul').toggle();
    e.stopPropagation();
    e.preventDefault();
});
});



/* dropdown */

/* sticky header */
  if ($(window).width() >= 992) {
 $(document).ready(function(){
      $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.homemenu').addClass('fixed fadeInDown animated');
        } else {
            $('.homemenu').removeClass('fixed fadeInDown animated');
        }
      });
});
};

$(document).ready(function(){
        if ($(window).width() >= 992 && $(window).width() <= 1199){
    var count_block = $('.moremenuh').length;
    var number_blocks = 5;
    //console.log(count_block);
    if(count_block < number_blocks){
        return false; 
    }
    else {
        $('.moremenuh').each(function(i,n){
            $('moremenuh').addClass(i);
            if(i == number_blocks) {
            $(this).append('<li class="view_more my-menu"><a class="dropdown-toggle">More</i></a></li>');
            }
            if(i> number_blocks) {
            $(this).addClass('wr_hide_menu').hide();
            }
        });
        $('.view_more').click(function() {
            $(this).toggleClass('active');
            $('.wr_hide_menu').slideToggle();
        });
    }
}
});


$(document).ready(function(){
        if ($(window).width() >= 1200 && $(window).width() <= 1409){
    var count_block = $('.moremenuh').length;
    var number_blocks = 5;
    //console.log(count_block);
    if(count_block < number_blocks){
        return false; 
    }
    else {
        $('.moremenuh').each(function(i,n){
            $('moremenuh').addClass(i);
            if(i == number_blocks) {
            $(this).append('<li class="view_more my-menu"><a class="dropdown-toggle">More</a></li>');
            }
            if(i> number_blocks) {
            $(this).addClass('wr_hide_menu').hide();
            }
        });
        $('.view_more').click(function() {
            $(this).toggleClass('active');
            $('.wr_hide_menu').slideToggle();
        });
    }
}
});

$(document).ready(function(){
       if ($(window).width() >= 1410){
    var count_block = $('.moremenuh').length;
    var number_blocks = 7;
    //console.log(count_block);
    if(count_block < number_blocks){
        return false; 
    }
    else {
        $('.moremenuh').each(function(i,n){
            $('moremenuh').addClass(i);
            if(i == number_blocks) {
            $(this).append('<li class="view_more my-menu"><a class="dropdown-toggle">More</a></li>');
            }
            if(i> number_blocks) {
            $(this).addClass('wr_hide_menu').hide();
            }
        });
        $('.view_more').click(function() {
            $(this).toggleClass('active');
            $('.wr_hide_menu').slideToggle();
        });
    }
}
});


/* sidemenu */
$(document).ready(function(){
$('#closeButton').on('click', function(e) {
    $(".topbsp").slideToggle('slow');
});
});

 $(document).ready(function(){
$('.loadmr').each(function(){
    var $ul = $(this),
        $lis = $ul.find('.product-thumb:gt(5)'),
        isExpanded = $ul.hasClass('expanded');
    $lis[isExpanded ? 'show' : 'hide']();
    
    if($lis.length > 0){
        $ul
            .append($('<div class="showmore text-xs-center"><li class="expand list-unstyled btn btn-primary">' + (isExpanded ? 'View Less' : 'load More') + '</li></div>')
            .click(function(event){
                var isExpanded = $ul.hasClass('expanded');
                event.preventDefault();
                $(this).html('<li class="expand list-unstyled btn btn-primary">' + (isExpanded ? 'load More' : 'load Less') + '</li>');
                $ul.toggleClass('expanded');
                $lis.toggle();
            }));
    }
});
});

 