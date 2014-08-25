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
    this.width = this.padding[0] - 2 * this.AREA_MARGIN + bottom_right[0] - top_left[0];
    this.height = this.padding[1] - 2 * this.AREA_MARGIN + bottom_right[1] - top_left[1];

    this.rotate = (this.height - this.width) > 2 && this.ALLOW_ROTATION;

    element.style.left = top_left[0] - this.padding[0] / 2 + this.AREA_MARGIN + "px";
    element.style.top = top_left[1] - this.padding[1] / 2 + this.AREA_MARGIN + "px";
    element.style.width = this.width + "px";
    element.style.height = this.height + "px";
}


HashtagGroup.prototype.opacity = function(maximum_count) {
    return 1 - (maximum_count - this.tags_count) / maximum_count;
}


HashtagGroup.prototype.setCanvasSize = function(shortest_word_width, font_size, lines_count) {
    // умножаем на 2, а то текст не пишется на границах
    if (this.rotate) {
        this.canvas.setAttribute('height', 2 * shortest_word_width);
        this.canvas.setAttribute('width', 2 * font_size * lines_count);
    }
    else {
        this.canvas.setAttribute('width', 2 * shortest_word_width);
        this.canvas.setAttribute('height', 2 * font_size * lines_count);
    }

    this.canvas.style.width = 2 * this.width + "px";
    this.canvas.style.height = 2 * this.height + "px";
}


HashtagGroup.prototype.drawTag = function(test_context, font_family) {
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

    this.setCanvasSize(shortest_word_width, font_size, lines.length);

    var context = this.canvas.getContext("2d");
    context.fillStyle = getColor(this.opacity(maximum_count));

    if (this.rotate)
        context.textAlign = 'center';
    else
        context.textAlign = 'left';

    context.textBaseline = 'top';
    context.font = font_size + 'px ' + font_family;

    var leftMargin = 0;
    if (this.rotate) {
        context.rotate(-Math.PI/2);
        leftMargin = width / 2.0 - width;
    }

    for (var j = 0; j < lines.length; j++)
        context.fillText(lines[j], leftMargin, font_size * j, shortest_word_width);
}