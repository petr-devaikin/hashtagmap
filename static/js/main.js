var MIN_LATITUDE = 55.492144;
var MIN_LONGITUDE = 37.235253;
var MAX_LATITUDE = 55.996804;
var MAX_LONGITUDE = 37.945527;

var MIN_OPACITY = 0.2;
var MAX_OPACITY = 1;

var PIXELS_PER_KM = 25;

window.onload = function() {
    var areas = document.getElementsByClassName('tag-area');
    for (i = 0; i < areas.length; i++) {
        var area_radius = parseInt(areas[i].getAttribute('radius'));
        var area_lat = MAX_LATITUDE - parseFloat(areas[i].getAttribute('latitude'));
        var area_long = parseFloat(areas[i].getAttribute('longitude')) - MIN_LONGITUDE;
        var area_lat_km = area_lat / lat_km;
        var area_long_km = area_long / long_km;

        areas[i].style.left = area_long_km * PIXELS_PER_KM + "px";
        areas[i].style.top = area_lat_km * PIXELS_PER_KM + "px";
        areas[i].style.width = area_radius / 1000 * 2 * PIXELS_PER_KM - 5 + "px";
        areas[i].style.height = area_radius / 1000 * 2 * PIXELS_PER_KM - 5 + "px";
        areas[i].style.opacity = MAX_OPACITY -
            (maximum_count - parseFloat(areas[i].getAttribute('count'))) / maximum_count *
            (MAX_OPACITY - MIN_OPACITY);
    }
}