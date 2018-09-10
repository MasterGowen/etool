$( document ).ready(
    function () {
        setTimeout(function () {
            $('.message').remove();
        }, 2000)

        $('.navbar-burger.burger').click(function () {
                $('.navbar-menu').toggle()
            })
    }
)