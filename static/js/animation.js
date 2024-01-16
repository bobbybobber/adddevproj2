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