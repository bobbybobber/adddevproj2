$(document).ready(function() {
  // Select the card rows
  var cardRows = $('.card-row');

  // Set initial position and opacity for rows
  cardRows.css({
    'transform': 'translateY(100px)',
    'opacity': '0'
  });

  // Animate each card row
  cardRows.each(function(index) {
    var cardRow = $(this);
    var delay = index * 200; // Adjust delay as needed

    // Use setTimeout to delay animations
    setTimeout(function() {
      cardRow.css({
        'transform': 'translateY(0)',
        'opacity': '1',
        'transition': 'transform 0.5s ease, opacity 0.5s ease'
      });
    }, delay);
  });
});
$(document).ready(function() {
  // Add a click event listener to all the anchor tags in the navbar
  $('#navbar a').on('click', function() {
    // Remove the 'active' class from all anchor tags
    $('#navbar a').removeClass('active');

    // Add the 'active' class to the clicked anchor tag
    $(this).addClass('active');
  });
});
<script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
$.ajax({
    type: 'POST',
    url: '/createblog',
    data: formData,
    processData: false,
    contentType: false,
    success: function (response) {
        // Update the carousel with the new blog card
        $('#dynamicCarousel').prepend(response.new_blog_card_html);

        // Initiate the redirect
        window.location.href = retrieveblog;
    }
});
  $(document).ready(function(){
        $('#profileCarousel').carousel();
        setInterval(function(){
            $('#profileCarousel').carousel('next');
        }, 3000); // Adjust the interval as needed (in milliseconds)
    });