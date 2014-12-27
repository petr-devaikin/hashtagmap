window.onload = function() {
    bind_info_button();
    set_full_map_size();
    load_map();

    draw_tags();

    set_scroll();
    move_map_to_center();
}

function bind_info_button() {
    var button = document.getElementById("info_button");
    var info = document.getElementById("info_block");
    button.onclick = function() {
        var style = window.getComputedStyle(info);
        if (style.display == "none")
            info.style.display = "block";
        else
            info.style.display = "none";
    }
}

var is_mouse_down = false;
var oldY = 0;
var oldX = 0;
var marginTop = 0;
var marginLeft = 0;

function set_scroll() {
    var main_container = document.getElementById("main_container");
    var main_width = main_container.offsetWidth;
    var main_height = main_container.offsetHeight;

    var map = document.getElementById("map_container");
    document.onmousedown = function(e) {
        is_mouse_down = true;
        oldY = e.pageY;
        oldX = e.pageX;
        return false;
    };
    document.onmouseup = function(e) {
        oldY = 0;
        oldX = 0;
        is_mouse_down = false;

        if (marginTop > 0)
            marginTop = 0;
        if (marginTop + main_height < window.innerHeight)
            marginTop = window.innerHeight - main_height;
        if (marginLeft > 0)
            marginLeft = 0;
        if (marginLeft + main_width < window.innerWidth)
            marginLeft = window.innerWidth - main_width;

        move_map(true);

        return false;
    };
    document.onmousemove = function(e) {
        if (is_mouse_down) {
            var newY = e.pageY;
            var newX = e.pageX;
            marginTop += newY - oldY;
            marginLeft += newX - oldX;
            oldY = newY;
            oldX = newX;
            move_map();
        }
    };
}
