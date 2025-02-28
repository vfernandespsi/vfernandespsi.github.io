//========= testimonial 
tns({
    container: '.testimonial-slider',
    items: 10,
    slideBy: 'page',
    autoplay: true,
    autoplayButtonOutput: false,
    mouseDrag: true,
    gutter: 0,
    nav: true,
    controls: false,
    controlsText: ['<i class="lni lni-arrow-left"></i>', '<i class="lni lni-arrow-right"></i>'],
    responsive: {
        0: {
            items: 1,
        },
        540: {
            items: 1,
        },
        768: {
            items: 1,
        },
        992: {
            items: 1,
        },
        1170: {
            items: 1,
        }
    }
});


//========= photo 
tns({
    container: '.photo-slider',
    items: 2,
    slideBy: 'page',
    autoplay: true,
    autoplayButtonOutput: false,
    autoplayTimeout: 7000,
    mouseDrag: true,
    gutter: 0,
    nav: false,
    controls: false,
    controlsText: ['<i class="lni lni-arrow-left"></i>', '<i class="lni lni-arrow-right"></i>'],
    responsive: {
        0: {
            items: 1,
        },
        540: {
            items: 1,
        },
        768: {
            items: 1,
        },
        992: {
            items: 1,
        },
        1170: {
            items: 1,
        }
    }
});
