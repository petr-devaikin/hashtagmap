var MAP_WIDTH = 640;
var MAP_HEIGHT = 640;

var MAP_LATITUDE = 0.1237;
var MAP_LONGITUDE = 0.2196;

if (location_name == "London") {
    MAP_LATITUDE = 0.1368;
    MAP_LONGITUDE = 0.2196;
}

var PIXELS_PER_LATITUDE = MAP_WIDTH / MAP_LATITUDE;
var PIXELS_PER_LONGITUDE = MAP_HEIGHT / MAP_LONGITUDE;

var FONT_FAMILY = 'sans-serif';


function draw_tags() {
    var test_canvas = document.getElementById('test_canvas');
    var test_context = test_canvas.getContext("2d");

    var size = get_position(MIN_LATITUDE, MAX_LONGITUDE);

    var tags_canvas = document.getElementById('tags_canvas');
    tags_canvas.setAttribute('width', size[0])
    tags_canvas.setAttribute('height', size[1])
    var tags_context = tags_canvas.getContext("2d");

    for (var i in groups) {
        var group = new HashtagGroup(groups[i]);
        group.drawTag(test_context, tags_context, FONT_FAMILY);
    }
}

