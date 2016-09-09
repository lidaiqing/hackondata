var DataLayer = (function () {
  google.maps.InfoWindow.prototype.isOpen = function () {
    var map = this.getMap();
    return (map !== null && typeof map !== "undefined");
  };

  function DataLayer (category, url, icon) {
    var _this = this;
    this.markers_ = {};
    this.url = url;
    this.icon = icon;
    // marker clustering
    this.mc = null;
    // overlapped markers
    this.oms = null;
    this.category = category;

    this.infoWindow = new google.maps.InfoWindow();
    this.infoWindow.addListener('domready', function () {
      _this.infoWindowReady(this);
    });
    this.infoWindow.addListener('closeclick', function () {
      _this.infoWindowClosed(this);
    });
    this.infoWindow._close = this.infoWindow.close;
    this.infoWindow.close = function () {
      _this.infoWindowClosed(this);
      this._close();
    };
    this.infoWindow.marker = null;

    this.layer = new google.maps.Data();
  }

  DataLayer.prototype = new google.maps.OverlayView();

  DataLayer.prototype.updateMarkersMap = function () {
    var fid, marker;
    if (this.infoWindow) {
      this.infoWindow.close();
    }
    this.layer.setMap(this.getMap());
    for (fid in this.markers_) {
      if (this.markers_.hasOwnProperty(fid)) {
        marker = this.markers_[fid];
        marker.setMap(this.getMap());
        marker.setVisible(!!this.getMap());
      }
    }
    if (this.mc) {
      this.mc.repaint();
    }
  };

  DataLayer.prototype.onAdd = function () {
    this.updateMarkersMap();
  };

  DataLayer.prototype.onRemove = function () {
    this.updateMarkersMap();
  };

  DataLayer.prototype.draw = function () {

  };

  DataLayer.prototype.loadData = function () {
    var _this = this;
    return $.getJSON(
      this.url,
      function (data) {
        _this.proccessGeoJson(data);
      }
    );
  };

  DataLayer.prototype.proccessGeoJson = function (data) {
    this.addGeoJson(data);
  };

  DataLayer.prototype.addGeoJson = function (data) {
    var tempLayer = new google.maps.Data(),
      features = tempLayer.addGeoJson(data),
      i,
      mapFeatures = {},
      fid,
      feature,
      removed = 0,
      _this = this;

    for (i = 0; i < features.length; i++) {
      feature = features[i];
      if (feature.getGeometry().getType() === "Point") {
          fid = String(features[i].getProperty("id"));
          mapFeatures[fid] = data.features[i];
      }
    }

    for (i = 0; i < features.length; i = i + 1) {
      feature = features[i];
      if (feature.getGeometry().getType() === "Point") {
        this.addMarker(feature);
      }
    }
  };

  DataLayer.prototype.addMarker = function (feature) {
    var _this = this,
      fid = String(feature.getProperty('id')),
      marker;
      marker = new google.maps.Marker({
        position: feature.getGeometry().get(),
        map: this.getMap(),
        icon: this.icon,
        visible: true
      });
      marker.feature = feature;
      this.markers_[fid] = marker;
      if (this.mc) {
        this.mc.addMarker(marker);
      }
      if (this.oms) {
        this.oms.addMarker(marker);
      }

      google.maps.event.addListener(marker, 'click',
        (function (marker) {
          return function () {
            if (!_this.infoWindow || !_this.getMap()) {
              return;
            }
            if (_this.getMap().hasOwnProperty('closeAllInfoWindows')) {
              _this.getMap().closeAllInfoWindows();
            }
            _this.infoWindow.setContent(_this.genContent(marker.feature));
            _this.infoWindow.open(_this.getMap(), marker);
            _this.infoWindow.marker = marker;
          };
        })(marker));
  };
  DataLayer.prototype.infoWindowReady = function (infoWindow) {

  };

  DataLayer.prototype.infoWindowClosed = function (infoWindow) {

  };
  return DataLayer;
}());
