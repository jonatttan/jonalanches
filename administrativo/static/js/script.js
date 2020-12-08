$(function () {
  'use strict'

  $('[data-toggle="offcanvas"]').on('click', function () {
    $('.offcanvas-collapse').toggleClass('open')
  })
})

/*
var inputs = document.querySelectorAll('input');

function verificar() {
    return [].filter.call(inputs, function (input) {
        return input.checked;
    }).length;
}
document.querySelector('button').addEventListener('click', function () {
    var valido = verificar();
    if (!valido) alert('Falta escolher uma checkbox!');
    else alert('Tudo ok!');
});
*/