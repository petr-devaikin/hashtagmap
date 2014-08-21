var MAP_ZOOM = 12;

function get_map_url(latitude, longitude) {
    return "http://maps.googleapis.com/maps/api/staticmap?center=" +
        latitude + "," + longitude + "&zoom=" + MAP_ZOOM + "&scale=2" +
        "&size=" + MAP_WIDTH + "x" + MAP_HEIGHT + "&maptype=roadmap" +
        "&style=element:labels%7Cvisibility:off" +
        "&style=element:geometry.stroke%7Cvisibility:off" +

        "&style=feature:landscape%7Cvisibility:off" +

        "&style=feature:poi%7Cvisibility:off" +
        "&style=feature:poi.park%7Cvisibility:on" +
        "&style=feature:poi.park%7Clightness:90" +
        "&style=feature:poi.park%7Csaturation:-100" +


        "&style=feature:road%7Csaturation:-100" +
        "&style=feature:road.local%7Clightness:30" +
        "&style=feature:road.arterial%7Clightness:30" +
        "&style=feature:road.highway%7Clightness:30" +
        //"&style=feature:road.local%7Cvisibility:off" +

        "&style=feature:transit%7Cvisibility:off" +
        "&style=feature:water%7Clightness:50" +
        //"&style=element:geometry.fill&7feature:road%7Cvisibility:off" +
        "&key=" + map_key;
}

function create_img(latitude, longitude) {
    var img = document.createElement('div');
    img.style.background = "url('" + get_map_url(latitude, longitude) + "') 0 0 no-repeat";
    img.style.backgroundSize = MAP_WIDTH + "px " + MAP_WIDTH + "px";
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
    var map = document.getElementById("map_container");
    var main = document.getElementById("main_container");
    map.style.width = size[0] + "px";
    map.style.height = size[1] + "px";
    main.style.width = size[0] + "px";
    main.style.height = size[1] + "px";
}


function move_map_to_center() {
    var main_container = document.getElementById("main_container");
    marginTop = -(main_container.offsetHeight - window.innerHeight) / 2;
    marginLeft = -(main_container.offsetWidth - window.innerWidth) / 2;
    move_map();
}

function move_map(animation) {
    $(main_container).stop();
    if (animation)
        $(main_container).animate({
            top: marginTop,
            left: marginLeft
        }, "medium");
    else {
        main_container.style.top = marginTop + "px";
        main_container.style.left = marginLeft + "px";
    }
}