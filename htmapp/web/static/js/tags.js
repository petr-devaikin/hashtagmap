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

