function get_map_url(latitude, longitude) {
    return "http://maps.googleapis.com/maps/api/staticmap?center=" +
        latitude + "," + longitude + "&zoom=" + MAP_ZOOM + "&scale=2" +
        "&size=" + MAP_WIDTH + "x" + MAP_HEIGHT + "&maptype=roadmap" +
        "&style=element:labels%7Cvisibility:off&style=saturation:0&key=" + MAP_KEY;
}

function create_img(latitude, longitude) {
    var img = document.createElement('img');
    img.setAttribute('src', get_map_url(latitude, longitude));
    img.classList.add("map_part");
    return img;
}

function add_backgroud() {
    var longitude = MIN_LONGITUDE;
    var x = 0;
    while (longitude <= MAX_LONGITUDE) {
        var latitude = MAX_LATITUDE;
        var y = 0;
        while (latitude > MIN_LATITUDE) {
            var img = create_img(latitude - MAP_LATITUDE / 2, longitude + MAP_LONGITUDE / 2);
            img.style.left = x + "px";
            img.style.top = y + "px";
            document.getElementById("map_container").appendChild(img);

            latitude -= MAP_LATITUDE;
            y += MAP_HEIGHT;
        }

        longitude += MAP_LONGITUDE;
        x += MAP_WIDTH;
    }
}

function set_full_map_size() {
    var size = get_position(MIN_LATITUDE, MAX_LONGITUDE);
    document.getElementById("map_container").style.width = size[0] + "px";
    document.getElementById("map_container").style.height = size[1] + "px";
}