var MIN_LATITUDE = 55.485;
var MAX_LATITUDE = 56.01;

var MIN_LONGITUDE = 37.225;
var MAX_LONGITUDE = 37.957;

var MAP_ZOOM = 12;


var MAP_WIDTH = 640;
var MAP_HEIGHT = 640;

var MAP_LATITUDE = 0.1237;
var MAP_LONGITUDE = 0.2196; // 92 - 94

var PIXELS_PER_KM = 35;
var PIXELS_PER_LATITUDE = MAP_WIDTH / MAP_LATITUDE;
var PIXELS_PER_LONGITUDE = MAP_HEIGHT / MAP_LONGITUDE;

var FONT_FAMILY = 'sans serif';


function draw_tags() {
    var test_canvas = document.getElementById('test_canvas');
    var test_context = test_canvas.getContext("2d");

    var areas = document.getElementsByClassName('tag_area');
    for (i = 0; i < areas.length; i++) {
        var group = new HashtagGroup(areas[i]);
        group.drawTag(test_context);
    }
}

