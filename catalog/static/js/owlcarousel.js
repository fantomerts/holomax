$(function() {
    // Owl Carousel
    var movieOwl = $(".movies__carousel");
    movieOwl.owlCarousel({
        // responsive : {
        //     //breakpoint from 0 and up
        //     0 : {
        //         stagePadding: 0
        //     },
        //     375 : {
        //         stagePadding: 20
        //     },
        //     440 : {
        //         stagePadding: 0
        //     },
        //     600 : {
        //         stagePadding: 30
        //     },
        //     992: {
        //     },
        //     // add as many breakpoints as desired , breakpoint from 480 up
        //     1400 : {
        //     },
        // },
        //loop: true,
        nav: false,
        dots: false,
        autoWidth: true,
        margin: 25,
        slideBy: 5,
        //dotsContainer: '#carousel-custom-dots',
        //navContainer: '#carousel-custom-nav',
        //navText : ["<i class='fa fa-arrow-left' aria-hidden='true'></i>","<i class='fa fa-arrow-right' aria-hidden='true'></i>"]
    });


    $('.movies__move-left').click(function() {
        movieOwl.trigger('prev.owl.carousel', [300]);
    })
    // Go to the previous item
    $('.movies__move-right').click(function() {
        movieOwl.trigger('next.owl.carousel');
    })
});

$(function() {
    // Owl Carousel
    var seanceOwl = $(".seances__carousel");
    seanceOwl.owlCarousel({
        // responsive : {
        //     //breakpoint from 0 and up
        //     0 : {
        //         stagePadding: 0
        //     },
        //     375 : {
        //         stagePadding: 20
        //     },
        //     440 : {
        //         stagePadding: 0
        //     },
        //     600 : {
        //         stagePadding: 30
        //     },
        //     992: {
        //     },
        //     // add as many breakpoints as desired , breakpoint from 480 up
        //     1400 : {
        //     },
        // },
        //loop: true,
        nav: false,
        dots: false,
        autoWidth: true,
        margin: 20,
        // slideBy: 5,
        slideBy: 2,
        //dotsContainer: '#carousel-custom-dots',
        //navContainer: '#carousel-custom-nav',
        //navText : ["<i class='fa fa-arrow-left' aria-hidden='true'></i>","<i class='fa fa-arrow-right' aria-hidden='true'></i>"]
    });


    $('.seances__move-left').click(function() {
        seanceOwl.trigger('prev.owl.carousel', [300]);
    })
    // Go to the previous item
    $('.seances__move-right').click(function() {
        seanceOwl.trigger('next.owl.carousel');
    })
});