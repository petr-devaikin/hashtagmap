function paintLegend() {
    var groups = document.querySelectorAll('#legend .legendGroup');
    for (var i = 0; i < groups.length; i++) {
        var v = groups[i].getAttribute('v');
        groups[i].style.borderBottomColor = getColor(v);
    }
}