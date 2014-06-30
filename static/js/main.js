var MIN_LATITUDE = 55.492144;
var MIN_LONGITUDE = 37.235253;
var MAX_LATITUDE = 55.996804;
var MAX_LONGITUDE = 37.945527;

var MIN_OPACITY = 0.2;
var MAX_OPACITY = 1;

var PIXELS_PER_KM = 35;

var FONT_HEIGHT = 12;

window.onload = function() {
    var areas = document.getElementsByClassName('tag-area');
    for (i = 0; i < areas.length; i++) {
        var area_radius = parseInt(areas[i].getAttribute('radius'));
        var area_lat = MAX_LATITUDE - parseFloat(areas[i].getAttribute('latitude'));
        var area_long = parseFloat(areas[i].getAttribute('longitude')) - MIN_LONGITUDE;
        var area_lat_km = area_lat / lat_km;
        var area_long_km = area_long / long_km;
        var tag = areas[i].getAttribute('tag')
        var canvas_id = areas[i].getAttribute('area-id');

        var width = area_radius / 1000 * 2 * PIXELS_PER_KM;

        var canvas = document.getElementById('canvas_' + canvas_id);
        var context = canvas.getContext("2d");
        context.font = FONT_HEIGHT + 'px Arial';
        context.fillStyle = '#000';
        context.textAlign = 'left';
        context.textBaseline = 'top';

        var measured = context.measureText(tag);
        if (measured.width > FONT_HEIGHT) {
            var s = tag.substring(0, tag.length / 2);
            var f = tag.substring(tag.length / 2);
            context.fillText(s, 0, 0, width)
            context.fillText(f, 0, 12, width)
        }
        else
            context.fillText(tag, 0, 0, width);

        areas[i].style.left = area_long_km * PIXELS_PER_KM + "px";
        areas[i].style.top = area_lat_km * PIXELS_PER_KM + "px";
        areas[i].style.width = width + "px";
        areas[i].style.height = area_radius / 1000 * 2 * PIXELS_PER_KM + "px";
        //canvas.style.width = area_radius / 1000 * 2 * PIXELS_PER_KM + "px";
        //canvas.style.height = area_radius / 1000 * 2 * PIXELS_PER_KM + "px";
        //areas[i].style.opacity = MAX_OPACITY -
        //    (maximum_count - parseFloat(areas[i].getAttribute('count'))) / maximum_count *
        //    (MAX_OPACITY - MIN_OPACITY);
    }
}