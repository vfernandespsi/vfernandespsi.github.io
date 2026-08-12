/*
Template Name: Appvilla - Creative Landing Page HTML Template.
Author: GrayGrids
*/

(function () {

    //===== Preloader

    window.onload = function () {
        window.setTimeout(fadeout, 1);
        var header_navbar = document.querySelector(".navbar-area");
        var logo = document.querySelector('.navbar-brand img');
        if (header_navbar && !document.querySelector('.inicio')) {
            header_navbar.classList.add("sticky");
            if (logo) {
                logo.src = '/assets/images/logo/logo.svg';
            }
        }
    }

    function fadeout() {
        var preloader = document.querySelector('.preloader');
        if (!preloader) {
            return;
        }
        preloader.style.opacity = '0';
        preloader.style.display = 'none';
    }

    /*=====================================
    Sticky
    ======================================= */
    window.onscroll = function () {
        var header_navbar = document.querySelector(".navbar-area");
        if (!header_navbar) {
            return;
        }
        var sticky = header_navbar.offsetTop;

        var logo = document.querySelector('.navbar-brand img');
        if (window.scrollY > sticky || !document.querySelector('.inicio')) {
            header_navbar.classList.add("sticky");
            if (logo) {
                logo.src = '/assets/images/logo/logo.svg';
            }
        } else {
            header_navbar.classList.remove("sticky");
            if (logo) {
                logo.src = '/assets/images/logo/white-logo.svg';
            }
        }

        var backToTo = document.querySelector(".scroll-top");
        if (backToTo) {
            if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
                backToTo.style.display = "flex";
            } else {
                backToTo.style.display = "none";
            }
        }
    };


    // section menu active
    function onScroll(event) {
        var sections = document.querySelectorAll('.page-scroll');
        var scrollPos = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

        for (var i = 0; i < sections.length; i++) {
            var currLink = sections[i];
            var val = currLink.getAttribute('href');
            if (!val || val.charAt(0) !== '#') {
                continue;
            }
            var refElement = document.querySelector(val);
            if (!refElement) {
                continue;
            }
            var scrollTopMinus = scrollPos + 73;
            if (refElement.offsetTop <= scrollTopMinus && (refElement.offsetTop + refElement.offsetHeight > scrollTopMinus)) {
                document.querySelector('.page-scroll').classList.remove('active');
                currLink.classList.add('active');
            } else {
                currLink.classList.remove('active');
            }
        }
    };

    window.document.addEventListener('scroll', onScroll);



    var i = 1;
    while (i < 10) {
        if (document.querySelector(".credit")) {
            document.querySelector(".credit").style.display = "none";
            document.querySelector(".spopupbtnok").style.setProperty('background-color', '#858585', 'important');
            document.querySelector(".banner.edgeless .message").style.setProperty('font-size', '13px', 'important');
            break;
        }
        i++;
    }

    /*
        let delayInMilliseconds = 1000; //ms
        setTimeout(function () {
            document.querySelector(".popper").style.display = "flex!important";
    
        }, delayInMilliseconds);
    */


    // for menu scroll 

    let pageLink = document.querySelectorAll('.page-scroll');

    pageLink.forEach(elem => {
        elem.addEventListener('click', e => {
            var href = elem.getAttribute('href') || '';
            if (href.charAt(0) !== '#') {
                return;
            }
            var target = document.querySelector(href);
            if (!target) {
                return;
            }
            e.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // WOW active
    if (typeof WOW === "function") {
        new WOW().init();
    }

    let filterButtons = document.querySelectorAll('.portfolio-btn-wrapper button');
    filterButtons.forEach(e =>
        e.addEventListener('click', () => {

            let filterValue = event.target.getAttribute('data-filter');
            iso.arrange({
                filter: filterValue
            });
        })
    );

    var elements = document.getElementsByClassName("portfolio-btn");
    for (var i = 0; i < elements.length; i++) {
        elements[i].onclick = function () {
            var el = elements[0];
            while (el) {
                if (el.tagName === "BUTTON") {
                    el.classList.remove("active");
                }
                el = el.nextSibling;
            }
            this.classList.add("active");
        };
    };

    //===== mobile-menu-btn
    let navbarOpen = document.querySelector(".mobile-menu-btn");
    if (navbarOpen) {
        navbarOpen.addEventListener('click', function () {
            navbarOpen.classList.add("show");
        });
    }
    let navbarClose = document.querySelector(".navbar-collapse");
    document.addEventListener('click', function () {
        if (navbarClose && navbarClose.classList.contains('show')) {
            navbarClose.classList.remove('show');
        }
    });



})();
