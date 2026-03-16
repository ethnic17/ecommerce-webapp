$(document).ready(function () {

    // Lift card and show stats on Mouseover
    $('#product-card').hover(
        function () {
            $(this).addClass('animate');
            $('div.carouselNext, div.carouselPrev').addClass('visible');
        },
        function () {
            $(this).removeClass('animate');
            $('div.carouselNext, div.carouselPrev').removeClass('visible');
        }
    );


    /* ---- Image Gallery Carousel ---- */

    var carousel = $('#carousel ul');
    var carouselSlideWidth = 335;
    var carouselWidth = 0;
    var isAnimating = false;

    // Build carousel width
    $('#carousel li').each(function () {
        carouselWidth += carouselSlideWidth;
    });

    $(carousel).css('width', carouselWidth);


    // Load Next Image
    $('div.carouselNext').on('click', function () {

        var currentLeft = Math.abs(parseInt($(carousel).css("left")));
        var newLeft = currentLeft + carouselSlideWidth;

        if (newLeft == carouselWidth || isAnimating === true) {
            return;
        }

        $('#carousel ul').css({
            'left': "-" + newLeft + "px",
            "transition": "300ms ease-out"
        });

        isAnimating = true;

        setTimeout(function () {
            isAnimating = false;
        }, 300);

    });


    // Load Previous Image
    $('div.carouselPrev').on('click', function () {

        var currentLeft = Math.abs(parseInt($(carousel).css("left")));
        var newLeft = currentLeft - carouselSlideWidth;

        if (newLeft < 0 || isAnimating === true) {
            return;
        }

        $('#carousel ul').css({
            'left': "-" + newLeft + "px",
            "transition": "300ms ease-out"
        });

        isAnimating = true;

        setTimeout(function () {
            isAnimating = false;
        }, 300);

    });

});