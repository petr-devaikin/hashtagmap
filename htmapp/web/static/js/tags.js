var MIN_LATITUDE = 55.485;
var MAX_LATITUDE = 56.01;

var MIN_LONGITUDE = 37.225;
var MAX_LONGITUDE = 37.957;

var MAP_ZOOM = 12;

var MIN_OPACITY = 0;
var MAX_OPACITY = 1;

var MAP_WIDTH = 640;
var MAP_HEIGHT = 640;

var MAP_LATITUDE = 0.1237;
var MAP_LONGITUDE = 0.2196; // 92 - 94

var PIXELS_PER_KM = 35;
var PIXELS_PER_LATITUDE = MAP_WIDTH / MAP_LATITUDE;
var PIXELS_PER_LONGITUDE = MAP_HEIGHT / MAP_LONGITUDE;

var FONT_FAMILY = 'sans serif';
var AREA_MARGIN = 4;

var ALLOW_ROTATION = true;

function get_position(latitude, longitude) {
    return [PIXELS_PER_LONGITUDE * (longitude - MIN_LONGITUDE),
        PIXELS_PER_LATITUDE * (MAX_LATITUDE - latitude)];
}

function km_to_pixels(width, height) {
    return [long_km * width * PIXELS_PER_LONGITUDE,
        lat_km * height * PIXELS_PER_LATITUDE];
}

function draw_tags() {
    var test_canvas = document.getElementById('test_canvas');
    var test_context = test_canvas.getContext("2d");

    var areas = document.getElementsByClassName('tag_area');
    for (i = 0; i < areas.length; i++) {
        var area_radius = parseInt(areas[i].getAttribute('radius'));
        //var area_lat = parseFloat(areas[i].getAttribute('latitude'));
        //var area_long = parseFloat(areas[i].getAttribute('longitude'));
        var area_north = parseFloat(areas[i].getAttribute('north'));
        var area_south = parseFloat(areas[i].getAttribute('south'));
        var area_west = parseFloat(areas[i].getAttribute('west'));
        var area_east = parseFloat(areas[i].getAttribute('east'));
        var area_top_left_position = get_position(area_north, area_west);
        var area_bottom_right_position = get_position(area_south, area_east);
        //var area_lat_km = area_lat / lat_km;
        //var area_long_km = area_long / long_km;
        var tag = areas[i].getAttribute('tag').toUpperCase();
        var tags_count =  parseFloat(areas[i].getAttribute('count'));
        var canvas_id = areas[i].getAttribute('area-id');

        var opacity = MAX_OPACITY - 
            (maximum_count - tags_count) /
            maximum_count * (MAX_OPACITY - MIN_OPACITY);

        var area_padding = km_to_pixels(area_radius / 1000.0 * 2, area_radius / 1000.0 * 2);
        var area_width = area_padding[0] - 2 * AREA_MARGIN +
                        area_bottom_right_position[0] - area_top_left_position[0];
        var area_height = area_padding[1] - 2 * AREA_MARGIN +
                        area_bottom_right_position[1] - area_top_left_position[1];

        var rotate = area_width < area_height && ALLOW_ROTATION;
        if (rotate) {
            var tmp = area_width;
            area_width = area_height;
            area_height = tmp;
        }

        var lines = fit_word(tag, area_width, area_height, 24, test_context);
        var shortest_word = find_shortest_word(lines, 24, test_context);
        var font_size = find_font_size(shortest_word, area_width, test_context);

        var canvas = document.getElementById('canvas_' + canvas_id);
        // умножаем на 2, а то текст не пишется на границах
        var shortest_word_width = width_of_word(shortest_word, font_size, test_context)

        if (rotate) {
            canvas.setAttribute('height', 2 * shortest_word_width);
            canvas.setAttribute('width', 2 * font_size * lines.length);
        }
        else {
            canvas.setAttribute('width', 2 * shortest_word_width);
            canvas.setAttribute('height', 2 * font_size * lines.length);
        }

        var context = canvas.getContext("2d");
        context.fillStyle = getColor(opacity);

        if (rotate)
            context.textAlign = 'center';
        else
            context.textAlign = 'left';

        context.textBaseline = 'top';
        context.font = font_size + 'px ' + FONT_FAMILY;

        var leftMargin = 0;
        if (rotate) {
            context.rotate(-Math.PI/2);
            leftMargin = area_width / 2.0 - area_width;
        }

        for (var j = 0; j < lines.length; j++)
            context.fillText(lines[j], leftMargin, font_size * j, shortest_word_width);
        
        if (rotate) {
            var tmp = area_width;
            area_width = area_height;
            area_height = tmp;
        }

        areas[i].style.left = area_top_left_position[0] - area_padding[0] / 2 + AREA_MARGIN + "px";
        areas[i].style.top = area_top_left_position[1] - area_padding[1] / 2 + AREA_MARGIN + "px";
        areas[i].style.width = area_width + "px";
        areas[i].style.height = area_height + "px";

        canvas.style.width = 2 * area_width + "px";
        canvas.style.height = 2 * area_height + "px";

        //canvas.style.height = area_radius / 1000 * 2 * PIXELS_PER_KM + "px";
    }
}

function fit_word(word, width, height, font_size, context) {
    context.font = font_size + 'px ' + FONT_FAMILY;

    var K = 1.0 * height / width;
    var lines_count = 1;
    var lines = [word];

    var word_width = context.measureText(word).width;
    var k = 1.0 * font_size / word_width;
    while (k < K) {
        lines_count += 1;
        if (lines_count > word.length)
            break;

        lines = div_word_into_parts(word, lines_count, context);

        var min_width = 9999;
        for (var i = 0; i < lines_count; i++) {
            var w = context.measureText(lines[i]).width;
            if (w < min_width)
                min_width = w;
        }
        k = 1.0 * font_size * lines_count / min_width;
    }
    return lines;
}

function div_word_into_parts(word, lines_count, context) {
    var word_width = context.measureText(word).width;
    var lines = [];

    var current_letter = 0;
    var current_start_letter = current_letter;
    var prev_width = 0;
    var ideal_word_part_width = 1.0 * word_width / lines_count;
    for (var i = 0; i < lines_count - 1; i++) {
        var last_dif = 9999;
        var dif = ideal_word_part_width * (i + 1);
        while (dif < last_dif) {
            current_letter += 1;
            last_dif = dif;
            var sub_word = word.substring(current_start_letter, current_letter);
            var sub_width = context.measureText(sub_word).width;
            dif = Math.abs(prev_width + sub_width - ideal_word_part_width * (i + 1));
        }
        var word_to_push = word.substring(current_start_letter, current_letter - 1);
        lines.push(word_to_push);
        prev_width += context.measureText(word_to_push).width;
        current_letter = current_letter - 1;
        current_start_letter = current_letter;
    }
    lines.push(word.substring(current_start_letter));

    return lines;
}

function find_shortest_word(lines, font_size, context) {
    var res = undefined;
    for (var i = 0; i < lines.length; i++) {
        var i_length = width_of_word(lines[i], font_size, context);
        if (res === undefined || width_of_word(res, font_size, context) > i_length)
            res = lines[i];
    }
    return res;
}

function find_font_size(shortest_word, area_width, context) {
    var font_size = 4;
    var word_width = width_of_word(shortest_word, font_size, context);
    while (word_width < area_width) {
        font_size++;
        word_width = width_of_word(shortest_word, font_size, context);
    }
    return font_size;
}

function width_of_word(word, font_size, context) {
    context.font = font_size + 'px ' + FONT_FAMILY;
    return context.measureText(word).width;
}

function getColor(opacity) {
    var r = Math.floor(95 * Math.sqrt(opacity) + 150);
    var g = Math.floor(150 - 150 * Math.sqrt(opacity));
    var b = g;
    return 'rgb(' + r + ',' + g + ',' + b + ')';
    //var c = Math.floor(255 - 255 * opacity);
    //return 'rgb(' + c + ',' + c + ',' + c + ')';
}