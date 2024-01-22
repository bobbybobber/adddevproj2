$(document).ready(function() {
  // ... existing code ...
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

  // Add a click event listener to all the anchor tags in the navbar
  $('#navbar a').on('click', function() {
    // Remove the 'active' class from all anchor tags
    $('#navbar a').removeClass('active');

    // Add the 'active' class to the clicked anchor tag
    $(this).addClass('active');
  });

  // Carousel interval
  $('.carousel').carousel({
    interval: 2000 //changes the speed
  });

  // Ensure card-bodies are visible after the animations
  $('.blog-card').css({
    'opacity': '1',
    'transform': 'translateY(0)'
  });
});

//  $('form').submit(function (event) {
//    event.preventDefault(); // Prevent the default form submission behavior
//
//    // Create a new FormData object
//    var formData = new FormData();
//
//    // Get the values entered by the user in the form fields
//    var name = $('#name').val();
//    var comment = $('#comment').val();
//    var image = $('#image')[0].files[0]; // Assuming you want to upload a single file
//
//    // Append the values to the FormData object
//    formData.append('name', name);
//    formData.append('comment', comment);
//    formData.append('image', image);
//
//    // Now, you can send this formData in your AJAX request
//    $.ajax({
//      type: 'POST',
//      url: '/createblog',
//      data: formData,
//      processData: false,
//      contentType: false,
//      success: function (response) {
//        // Handle the response from the server
//        console.log('Blog created successfully:', response);
//      },
//      error: function (error) {
//        // Handle errors if the AJAX request fails
//        console.error('Error creating blog:', error);
//      },
//    });
//  });
//}); // Closing brace for $(document).ready(function() {
