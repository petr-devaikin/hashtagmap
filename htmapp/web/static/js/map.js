function load_map() {
    var styles = [
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

    var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});

    var mapOptions = {
        center: new google.maps.LatLng((MAX_LATITUDE + MIN_LATITUDE) / 2,
            (MAX_LONGITUDE + MIN_LONGITUDE) / 2),
        zoom: 12,
        mapTypeControlOptions: {
            mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style'],
        },
        disableDefaultUI: true,
    };
    var map = new google.maps.Map(document.getElementById("map_container"),
        mapOptions);

    map.mapTypes.set('map_style', styledMap);
    map.setMapTypeId('map_style');

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