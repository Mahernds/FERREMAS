function showScrollButton() {
  if (
    document.body.scrollTop > 500 ||
    document.documentElement.scrollTop > 500
  ) {
    scrollBtn.style.display = "block";
  } else {
    scrollBtn.style.display = "none";
  }
}

function disableScrolling(){
  $("body").addClass("stop-scrolling");

}

function goTop() {
  window.scroll(0, 0, "auto");
}

// When the user scrolls down 20px from the top of the document, show the button
$(window).scroll(function () {
  showScrollButton();
});

$("#scrollBtn").click(function (e) {
  goTop();
});
