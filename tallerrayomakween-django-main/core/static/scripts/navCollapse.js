$("main").click(function (e) {
  e.preventDefault();
  let navAbierto = $("#navbarCollapse").hasClass("show");
  if (navAbierto) {
    $(".navbar-toggler").trigger("click");
  }
});
