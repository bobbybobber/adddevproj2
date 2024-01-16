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