$(document).ready(function () {

    /*Login page Body height */
    $('body.loginBg').height('');
    var bodyHeight = $('body.loginBg').outerHeight();
    $('body.loginBg').height(bodyHeight);

    /* Pasword hide show*/
    $('.passIcon').click(function () {
        $(this).toggleClass('fa-eye');
        var x = document.getElementById("password");
        if (x.type === "password") {
            x.type = "text";
        } else {
            x.type = "password";
        }
    });


    /* Top Tab Script */
    $('.coinList li').click(function () {
        var coinTab = $(this).attr('data-coin');
        $(this).parents('.whiteBox').find('.coinTabActive').removeClass('coinTabActive');
        $(this).addClass('coinTabActive');
        $('#' + coinTab).addClass('coinTabActive');
    });

    /* Second Tab */
    $('.tabList li').click(function () {
        var typeId = $(this).attr('data-type');
        $(this).parent().parent().find('.tabActive').removeClass('tabActive');
        $(this).addClass('tabActive');
        $('#' + typeId).addClass('tabActive');
    });

    /* submenu toggle */
    $(document).on('click','.dropClick', function () {
        if (!$(this).parent('.dropdownSlide').hasClass('openBox')) {
            $('.dropdownSlide').removeClass('openBox');
            $('.dropClick').removeClass('active');
        }
        if ($(this).parent('.dropdownSlide').hasClass('openBox')) {
            $(this).removeClass('active');
            $(this).parent('.dropdownSlide').removeClass('openBox');
        } else {
            $(this).addClass('active');
            $(this).parent('.dropdownSlide').addClass('openBox');
        }
    });

    $(document).mouseup(function (e) {
        var popup = $(".dropdownSlide");
        if (!$('.dropdownSlide').is(e.target) && !popup.is(e.target) && popup.has(e.target).length == 0) {
            popup.removeClass('openBox');
            $('.dropdownClick').removeClass('active');
        }
    });
});

$(window).resize(function () {
    $('body.loginBg').height('');
    var bodyHeight = $('body.loginBg').outerHeight();
    $('body.loginBg').height(bodyHeight);
});


/* Chart function*/
