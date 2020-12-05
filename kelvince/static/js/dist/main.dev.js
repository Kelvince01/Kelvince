"use strict";

var date = new Date();
document.querySelector('#year').innerHTML = date.getFullYear();
setTimeout(function () {
  $('#message').fadeOut('slow');
}, 3000);
var signUpButton = document.getElementById('signUp');
var signInButton = document.getElementById('signIn');
var container = document.getElementById('container');
signUpButton.addEventListener('click', function () {
  container.classList.add("right-panel-active");
});
signInButton.addEventListener('click', function () {
  container.classList.remove("right-panel-active");
});
$('.menu-bar').on('click', function () {
  $('nav ul').toggleClass('reveal');
});
$("body").on("click", function (event) {
  var $target = $(event.target);

  if (!$target.parents().is("details") && !$target.is("details")) {
    $("body").find("details").removeAttr("open");
  }
});