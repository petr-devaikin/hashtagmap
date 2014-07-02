var MIN_LATITUDE = 55.492144;
var MIN_LONGITUDE = 37.235253;
var MAX_LATITUDE = 55.996804;
var MAX_LONGITUDE = 37.945527;

var MIN_OPACITY = 0.2;
var MAX_OPACITY = 1;

var PIXELS_PER_KM = 35;

var FONT_FAMILY = 'Arial';
var AREA_PADDING = 2;

window.onload = function() {
    var test_canvas = document.getElementById('test_canvas');
    var test_context = test_canvas.getContext("2d");

    var areas = document.getElementsByClassName('tag-area');
    for (i = 0; i < areas.length; i++) {
        var area_radius = parseInt(areas[i].getAttribute('radius'));
        var area_lat = MAX_LATITUDE - parseFloat(areas[i].getAttribute('latitude'));
        var area_long = parseFloat(areas[i].getAttribute('longitude')) - MIN_LONGITUDE;
        var area_lat_km = area_lat / lat_km;
        var area_long_km = area_long / long_km;
        var tag = areas[i].getAttribute('tag').toUpperCase();
        var tags_count =  parseFloat(areas[i].getAttribute('count'));
        var canvas_id = areas[i].getAttribute('area-id');

        var opacity = MAX_OPACITY - 
            (maximum_count - tags_count) /
            maximum_count * (MAX_OPACITY - MIN_OPACITY);

        var area_width = area_radius / 1000.0 * 2 * PIXELS_PER_KM - 2 * AREA_PADDING;
        var area_height = area_radius / 1000.0 * 2 * PIXELS_PER_KM - 2 * AREA_PADDING;

        var lines = fit_word(tag, area_width, area_height, 24, test_context);
        var shortest_word = find_shortest_word(lines, 24, test_context);
        var font_size = find_font_size(shortest_word, area_width, test_context);

        var canvas = document.getElementById('canvas_' + canvas_id);
        // умножаем на 2, а то текст не пишется на границах
        var shortest_word_width = width_of_word(shortest_word, font_size, test_context)
        canvas.setAttribute('width', 2 * shortest_word_width);
        canvas.setAttribute('height', 2 * font_size * lines.length);

        var context = canvas.getContext("2d");
        context.fillStyle = getColor(opacity);
        context.textAlign = 'left';
        context.textBaseline = 'top';
        context.font = font_size + 'px ' + FONT_FAMILY;

        for (var j = 0; j < lines.length; j++) {
            context.fillText(lines[j], 0, font_size * j, shortest_word_width);
        }


        areas[i].style.left = area_long_km * PIXELS_PER_KM + AREA_PADDING + "px";
        areas[i].style.top = area_lat_km * PIXELS_PER_KM + AREA_PADDING + "px";
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
    var c = Math.floor(255 - 255 * opacity);
    return 'rgb(' + c + ',' + c + ',' + c + ')';
}