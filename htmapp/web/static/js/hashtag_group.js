
var AREA_MARGIN = 5;
var ALLOW_ROTATION = true;

var DRAWIND_FONT_SIZE = 24;
var FONT_FAMILY = 'sans serif';

var MIN_OPACITY = 0;
var MAX_OPACITY = 1;



function km_to_pixels(width, height) {
    return [long_km * width * PIXELS_PER_LONGITUDE,
        lat_km * height * PIXELS_PER_LATITUDE];
}

function get_position(latitude, longitude) {
    return [PIXELS_PER_LONGITUDE * (longitude - MIN_LONGITUDE),
        PIXELS_PER_LATITUDE * (MAX_LATITUDE - latitude)];
}

function HashtagGroup(element) {
    this.radius = parseInt(element.getAttribute('radius'));

    var north = parseFloat(element.getAttribute('north'));
    var south = parseFloat(element.getAttribute('south'));
    var west = parseFloat(element.getAttribute('west'));
    var east = parseFloat(element.getAttribute('east'));

    var bottom_right = get_position(south, east);
    var top_left = get_position(north, west);

    this.tag = element.getAttribute('tag').toUpperCase();
    this.tags_count =  parseFloat(element.getAttribute('count'));
    
    this.canvas = document.getElementById("canvas_" + element.getAttribute('area-id'));

    this.padding = km_to_pixels(this.radius / 1000.0 * 2, this.radius / 1000.0 * 2);
    this.width = this.padding[0] - 2 * AREA_MARGIN + bottom_right[0] - top_left[0];
    this.height = this.padding[1] - 2 * AREA_MARGIN + bottom_right[1] - top_left[1];

    this.rotate = (this.height - this.width) > 2 && ALLOW_ROTATION;

    element.style.left = top_left[0] - this.padding[0] / 2 + AREA_MARGIN + "px";
    element.style.top = top_left[1] - this.padding[1] / 2 + AREA_MARGIN + "px";
    element.style.width = this.width + "px";
    element.style.height = this.height + "px";
}

HashtagGroup.prototype.opacity = function(max_opacity, min_opacity, maximum_count) {
    return max_opacity - (maximum_count - this.tags_count) / maximum_count * (max_opacity - min_opacity);
}

HashtagGroup.prototype.drawTag = function(test_context) {
    var width = this.width;
    var height = this.height;
    if (this.rotate) {
        width = this.height;
        height = this.width;
    }

    var lines = fit_word(this.tag, width, height, DRAWIND_FONT_SIZE, test_context);
    var shortest_word = find_shortest_word(lines, DRAWIND_FONT_SIZE, test_context);
    var font_size = find_font_size(shortest_word, width, test_context);

    // умножаем на 2, а то текст не пишется на границах
    var shortest_word_width = width_of_word(shortest_word, font_size, test_context)

    if (this.rotate) {
        this.canvas.setAttribute('height', 2 * shortest_word_width);
        this.canvas.setAttribute('width', 2 * font_size * lines.length);
    }
    else {
        this.canvas.setAttribute('width', 2 * shortest_word_width);
        this.canvas.setAttribute('height', 2 * font_size * lines.length);
    }

    var context = this.canvas.getContext("2d");
    context.fillStyle = getColor(this.opacity(MAX_OPACITY, MIN_OPACITY, maximum_count));

    if (this.rotate)
        context.textAlign = 'center';
    else
        context.textAlign = 'left';

    context.textBaseline = 'top';
    context.font = font_size + 'px ' + FONT_FAMILY;

    var leftMargin = 0;
    if (this.rotate) {
        context.rotate(-Math.PI/2);
        leftMargin = width / 2.0 - width;
    }

    for (var j = 0; j < lines.length; j++)
        context.fillText(lines[j], leftMargin, font_size * j, shortest_word_width);

    this.canvas.style.width = 2 * this.width + "px";
    this.canvas.style.height = 2 * this.height + "px";
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

var MIN_RED = 230;
var MAX_RED = 255;
var MIN_GREEN = 230;
var MAX_GREEN = 49;
var MIN_BLUE = 230;
var MAX_BLUE = 0;

function get_saturation(o) {
    return Math.pow(o, 0.5);
}

function getColor(opacity) {
    var r = Math.floor(MIN_RED + (MAX_RED - MIN_RED) * get_saturation(opacity));
    var g = Math.floor(MIN_GREEN + (MAX_GREEN - MIN_GREEN) * get_saturation(opacity));
    var b = Math.floor(MIN_BLUE + (MAX_BLUE - MIN_BLUE) * get_saturation(opacity));
    return 'rgb(' + r + ',' + g + ',' + b + ')';
    //var c = Math.floor(255 - 255 * opacity);
    //return 'rgb(' + c + ',' + c + ',' + c + ')';
}