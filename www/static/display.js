var map,
  myOptions,
  infowindow,
  infowindows = [],
  mc,
  oms,
  attraction;

$(window).resize(function () {
    var h = $(window).height();
    $('#map_canvas').css('height', h);
  }).resize();


function mapInit() {
  myOptions = {
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    zoom: 11,
    center: new google.maps.LatLng(43.725704, -79.447754)
  };

  map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);

  map.closeAllInfoWindows = function () {
    var i;
    for (i = 0; i < infowindows.length; i = i + 1) {
      infowindows[i].close();
    }
  };
  infowindow = new google.maps.InfoWindow();

  attraction = new DataLayer(
    "attraction",
    "/api/0.1/attraction"
  );
  attraction.setMap(map);
  infowindows.push(infowindow);
  infowindows.push(attraction.infoWindow);
  attraction.loadData();
}

jQuery(document).ready(function (){
  mapInit();
  var omsOption = {keepSpiderfied: true};
  oms = new OverlappingMarkerSpiderfier(map, omsOption);
  //global listener for oms

  //MarkerCluster
  var mcOptions = {
    gridSize: 30,
    maxZoom: 20,
    ignoreHidden: true,
    imagePath: "static/vendor/google-marker-clusterer-plus/images/m"
  };

  mc = new MarkerClusterer(map, [], mcOptions);
  attraction.oms = oms;
  attraction.mc = mc;
  attraction.setMap(map);
});
