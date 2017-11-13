const mobileWidth = 768;

// This function handles the hidden classes and takes care of scroll position
function catNavBar() {
  if( $(window).width() < mobileWidth ) {
    $("#leftArrow").removeClass("hidden");
    $("#rightArrow").removeClass("hidden");
    if ($(".active").length ) {
      $("#catNavContent").scrollLeft(0);
      $("#catNavContent")
        .scrollLeft($(".active").offset()['left']-$(".active").width()/2);
    }
  } else if ($(window).width() >= mobileWidth) {
    $("#leftArrow").addClass("hidden");
    $("#rightArrow").addClass("hidden");
  }
}

// Remove hidden class if window width is less than mobileWidth
if($(window).width() < mobileWidth){
  catNavBar();
}

// Check after resizing window
$(window).resize(catNavBar);

// Attach event listeners and scroll function to arrows
$("#leftArrow").on("click", function() {
  let scroll = $("#catNavContent").scrollLeft();
  $("#catNavContent").animate({
        scrollLeft: scroll - 200
    }, 500);
});
$("#rightArrow").on("click", function() {
  let scroll = $("#catNavContent").scrollLeft();
  $("#catNavContent").animate({
        scrollLeft: scroll + 200
    }, 500);
});
