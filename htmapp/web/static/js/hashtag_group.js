function km_to_pixels(width, height) {
    return [long_km * width * PIXELS_PER_LONGITUDE,
        lat_km * height * PIXELS_PER_LATITUDE];
}

function get_position(latitude, longitude) {
    return [PIXELS_PER_LONGITUDE * (longitude - MIN_LONGITUDE),
        PIXELS_PER_LATITUDE * (MAX_LATITUDE - latitude)];
}

HashtagGroup.prototype.AREA_MARGIN = 5;
HashtagGroup.prototype.ALLOW_ROTATION = true;
HashtagGroup.prototype.DRAWIND_FONT_SIZE = 24;

function HashtagGroup(element) {
    this.radius = element['radius'];

    var north = element['north'];
    var south = element['south'];
    var west = element['west'];
    var east = element['east'];

    var bottom_right = get_position(south, east);
    var top_left = get_position(north, west);

    this.tag = element['tag'].toUpperCase();
    this.tags_count =  element['count'];

    this.padding = km_to_pixels(this.radius / 1000.0 * 2, this.radius / 1000.0 * 2);
    this.left = top_left[0] - this.padding[0] / 2 + this.AREA_MARGIN;
    this.top = top_left[1] - this.padding[1] / 2 + this.AREA_MARGIN;
    this.width = this.padding[0] - 2 * this.AREA_MARGIN + bottom_right[0] - top_left[0];
    this.height = this.padding[1] - 2 * this.AREA_MARGIN + bottom_right[1] - top_left[1];

    this.rotate = (this.height - this.width) > 2 && this.ALLOW_ROTATION;
}

HashtagGroup.prototype.drawTag = function(test_context, drawing_context, font_family) {
    var width = this.width;
    var height = this.height;
    if (this.rotate) {
        width = this.height;
        height = this.width;
    }

    var lines = fit_word(this.tag, width, height, this.DRAWIND_FONT_SIZE, font_family, test_context);
    var shortest_word = find_shortest_word(lines, this.DRAWIND_FONT_SIZE, font_family, test_context);
    var font_size = find_font_size(shortest_word, width, font_family, test_context);
    var shortest_word_width = width_of_word(shortest_word, font_size, font_family, test_context)

    drawing_context.fillStyle = getColor(this.tags_count);

    if (this.rotate) {
        drawing_context.textAlign = 'center';
    }
    else {
        drawing_context.textAlign = 'left';
    }

    drawing_context.textBaseline = 'top';
    drawing_context.font = font_size + 'px ' + font_family;

    var vertical_scale = 1.0 * height / font_size / lines.length;

    var leftMargin = this.left,
        topMargin = this.top / vertical_scale;

    if (this.rotate) {
        drawing_context.rotate(-Math.PI/2);
        leftMargin = width / 2.0 - width - this.top;
        topMargin = this.left / vertical_scale
    }

    drawing_context.scale(1, vertical_scale);

    for (var j = 0; j < lines.length; j++) {
        drawing_context.fillText(lines[j], leftMargin, topMargin + font_size * j, shortest_word_width);
    }

    drawing_context.scale(1, 1 / vertical_scale);

    if (this.rotate)
        drawing_context.rotate(Math.PI/2);
}