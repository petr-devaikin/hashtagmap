
var mapCentre = new google.maps.LatLng((MAX_LATITUDE + MIN_LATITUDE) / 2,
            (MAX_LONGITUDE + MIN_LONGITUDE) / 2);

var mapStyles = [
    { elementType: 'labels', stylers: [{ visibility: 'off' }], },
    { elementType: 'geometry.stroke', stylers: [{ visibility: 'off' }], },
    { featureType: 'landscape', stylers: [{ lightness: 100 }], },
    { featureType: 'poi', stylers: [{ visibility: 'off' }], },
    {
        elementType: 'geometry.fill',
        featureType: 'poi.park',
        stylers: [{ visibility: 'on' }, { lightness: 90 }, { saturation: -100 }],
    },
    { featureType: 'road', stylers: [{ saturation: -100 }], },
    { featureType: 'road.local', stylers: [{ lightness: 60 }], },
    { featureType: 'road.arterial', stylers: [{ lightness: 60 }], },
    {
        elementType: 'geometry.stroke',
        featureType: 'road.arterial',
        stylers: [{ visibility: 'on' }],
    },
    { featureType: 'road.highway', stylers: [{ lightness: 60 }], },
    { featureType: 'transit', stylers: [{ visibility: 'off' }], },
    { featureType: 'water', stylers: [{ lightness: 50 }], },
];


function load_map() {
    var styledMap = new google.maps.StyledMapType(mapStyles, {name: "Styled Map"});

    var mapOptions = {
        center: mapCentre,
        zoom: MAP_ZOOM,
        mapTypeControlOptions: {
            mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style'],
        },
        disableDefaultUI: true,
    };

    var map = new google.maps.Map(document.getElementById("map_container"), mapOptions);

    var overlay = new google.maps.OverlayView();
    overlay.draw = function() {};
    overlay.setMap(map);

    google.maps.event.addListenerOnce(map, "idle", onMapLoaded);

    map.mapTypes.set('map_style', styledMap);
    map.setMapTypeId('map_style');


    function onMapLoaded() {
        var north = new google.maps.LatLng(MAX_LATITUDE, (MIN_LONGITUDE + MAX_LONGITUDE) / 2),
            south = new google.maps.LatLng(MIN_LATITUDE, (MIN_LONGITUDE + MAX_LONGITUDE) / 2),
            west = new google.maps.LatLng((MAX_LATITUDE + MIN_LATITUDE) / 2, MIN_LONGITUDE),
            east = new google.maps.LatLng((MAX_LATITUDE + MIN_LATITUDE) / 2, MAX_LONGITUDE);

        var mapCanvasProjection = overlay.getProjection();
        var northPoint = mapCanvasProjection.fromLatLngToDivPixel(north),
            southPoint = mapCanvasProjection.fromLatLngToDivPixel(south),
            westPoint = mapCanvasProjection.fromLatLngToDivPixel(west),
            eastPoint = mapCanvasProjection.fromLatLngToDivPixel(east);

        PIXELS_PER_LONGITUDE = (eastPoint.x - westPoint.x) / (MAX_LONGITUDE - MIN_LONGITUDE);
        PIXELS_PER_LATITUDE = (southPoint.y - northPoint.y) / (MAX_LATITUDE - MIN_LATITUDE);

        set_full_map_size();
        google.maps.event.trigger(map, 'resize');
        map.setCenter(mapCentre);

        draw_tags();
        move_map_to_center();
        set_scroll();
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
    main_container.style.top = marginTop + "px";
    main_container.style.left = marginLeft + "px";
}