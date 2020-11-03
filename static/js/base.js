// Add smooth scrolling to all links in navbar + footer link
$(document).ready(function(){
    $(".navbar a, footer a[href='#myPage'], #home a[href='#python']").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

        // Prevent default anchor click behavior
        event.preventDefault();

        // Store hash
        var hash = this.hash;

        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
        $('html, body').animate({
                scrollTop: $(hash).offset().top
                }, 900, function(){

                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });
        } // End if
    });
})


// add sliding effect
$(window).scroll(function() {
    $(".slideanim").each(function(){
        var pos = $(this).offset().top;

        var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
            $(this).addClass("slide");
        }
    });
});

$('#notes').keyup(function(){
     $.getJSON('/background_process/', {
          notes: $('input[name="notes"]').val(),
        }, function(data) {
          $("#result").html(data.result);
        });
    return false;
});
