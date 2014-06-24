var MIN_LATITUDE = 55.492144;
var MIN_LONGITUDE = 37.235253;
var MAX_LATITUDE = 55.996804;
var MAX_LONGITUDE = 37.945527;

var MIN_OPACITY = 0.4;
var MAX_OPACITY = 1;

window.onload = function() {
    var areas = document.getElementsByClassName('tag-area');
    for (i = 0; i < areas.length; i++) {
        areas[i].style.left = (parseFloat(areas[i].getAttribute('longitude')) - MIN_LONGITUDE) * 1500 + "px";
        areas[i].style.top = (parseFloat(areas[i].getAttribute('latitude')) - MIN_LATITUDE) * 1200 + "px";
        areas[i].style.opacity = MAX_OPACITY -
            (maximum_count - parseFloat(areas[i].getAttribute('count'))) / maximum_count *
            (MAX_OPACITY - MIN_OPACITY);
    }
}