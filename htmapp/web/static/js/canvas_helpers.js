var MIN_RED = 230;
var MAX_RED = 255;
var MIN_GREEN = 230;
var MAX_GREEN = 49;
var MIN_BLUE = 230;
var MAX_BLUE = 0;

function get_saturation(count) {
    var i = 0;
    while (count > legend[i].min && i < legend.length - 1) i++;
    return i / (legend.length);
}

function getColor(count) {
    var r = Math.floor(MIN_RED + (MAX_RED - MIN_RED) * get_saturation(count));
    var g = Math.floor(MIN_GREEN + (MAX_GREEN - MIN_GREEN) * get_saturation(count));
    var b = Math.floor(MIN_BLUE + (MAX_BLUE - MIN_BLUE) * get_saturation(count));
    return 'rgb(' + r + ',' + g + ',' + b + ')';
}

function fit_word(word, width, height, font_size, font_famity, context) {
    context.font = font_size + 'px ' + font_famity;

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

function find_shortest_word(lines, font_size, font_family, context) {
    var res = undefined;
    for (var i = 0; i < lines.length; i++) {
        var i_length = width_of_word(lines[i], font_size, font_family, context);
        if (res === undefined || width_of_word(res, font_size, font_family, context) > i_length)
            res = lines[i];
    }
    return res;
}

function find_font_size(shortest_word, area_width, font_family, context) {
    var font_size = 4;
    var word_width = width_of_word(shortest_word, font_size, font_family, context);
    while (word_width < area_width) {
        font_size++;
        word_width = width_of_word(shortest_word, font_size, font_family, context);
    }
    return font_size;
}

function width_of_word(word, font_size, font_family, context) {
    context.font = font_size + 'px ' + font_family;
    return context.measureText(word).width;
}