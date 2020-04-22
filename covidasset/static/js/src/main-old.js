//let apiHost = "https://covid19.cdacchn.in:8080";
let apiHost = "http://localhost:8080";
//let geoJsonPath = "/static/geojson/";
let geoJsonPath = "/home/boss/Downloads/covid-thamc/covid-thamc/static/geojson/";
blueMarkerIconUrl = "/home/boss/Downloads/covid-thamc/covid-thamc/static/images/marker-icon.png";

redMarkerIconUrl = "/home/boss/Downloads/covid-thamc/covid-thamc/static/images/marker-icon-red.png";

let stateName = "TamilNadu";

let defaultZoom = 7;

let stateCenter = [10.985378, 78.664046];

let stateBounds = [
    [14.314431, 81.331526],
    [8.063881, 76.314360]
];

let markers = [];

let urlStateJson = geoJsonPath.concat(stateName, ".json");

var MarkerIcon = L.Icon.extend({
    options: {
        iconSize: [30, 45],
        //shadowSize: [50, 64],
        //iconAnchor: [22, 94],
        //shadowAnchor: [4, 62],
        //popupAnchor: [-3, -76]
    }
});

var blueMarkerIcon = new MarkerIcon({ iconUrl: blueMarkerIconUrl });

var redMarkerIcon = new MarkerIcon({ iconUrl: redMarkerIconUrl });

let geojson = null;

let districtsJson = null;

let districtsMap = null;

let geoData = null;

let titleLayer = null;

let map = L.map('map', {
    keyboard: false,
    dragging: false,
    zoomControl: false,
    boxZoom: false,
    doubleClickZoom: false,
    scrollWheelZoom: false,
    tap: false,
    touchZoom: false,
}).setView(stateCenter, defaultZoom);

let info = L.control();

info.onAdd = function (map) {

    this._div = L.DomUtil.create('div', 'info');

    this.updateForDistrict();

    return this._div;
};

info.updateForDistrict = function (properties) {
    let dist;
    if (properties) {
        dist = stateData.filter(ele => ele.name == properties.DISTRICT)
        dist[0].freeBeds - dist[0].patients < 10 ? this._div.classList.add('ak-alert') : this._div.classList.remove('ak-alert');
    }

    this._div.innerHTML = (properties ?
        "".concat(
            '<h4>', properties.DISTRICT, '</h4>',
            "Health Centres: ", dist[0].healthCentres,
            ", Patients: ", dist[0].patients,
            ", Free Beds: ", dist[0].freeBeds
        ) : 'Hover over a district');
}

info.addTo(map);

function stateStyle(feature) {

    // console.log (feature.properties.DISTRICT);

    let patientsCount = stateData.filter ( ele => ele.name == feature.properties.DISTRICT )[0].patients;

    // console.log ( patientsCount );

    return {

        fillColor: getColor(patientsCount), weight: 1, opacity: 1,

        color: '#333333', dashArray: '', fillOpacity: 0.7,
    };
}

function districtStyle(feature) {

    return {

        fillColor: '#000000', weight: 2, opacity: 1,

        color: '#000000', dashArray: '', fillOpacity: 0,
    };
}

function getColor(d) {

    // console.log ( d )

    return d > 160 ? '#7F0000' : d > 120 ? '#B30000' : d > 80 ? '#E63300' : d > 40 ? '#F8782B' : d > 0 ? '#FFC080' : '#fff8f0';
}

function clearMarkers() {

    if (markers.length) {

        markers.forEach((marker) => {

            map.removeLayer(marker);
        });
    }
}

function onMouseOverDistrict(e) {

    var layer = e.target;

    layer.setStyle({ weight: 2, color: '#85ded8', dashArray: '', fillOpacity: 0.7 });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {

        layer.bringToFront();
    }

    console.log(layer.feature.properties.DISTRICT)

    info.updateForDistrict(layer.feature.properties);
}

function onMouseOutDistrict(e) {

    geojson.resetStyle(e.target);
}

function onClickDistrict(e) {

    let selectedDistrict = e.target.feature.properties.DISTRICT;

    console.log(selectedDistrict);

    titleLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 'attribution': 'Map data &copy; OpenStreetMap contributors' }).addTo(map);

    map.fitBounds(e.target.getBounds());

    geojson.clearLayers();

    let selectedDistrictGeoJson = geoData.features.filter(ele => ele.properties.DISTRICT == selectedDistrict);

    geojson = L.geoJson(selectedDistrictGeoJson, {

        style: districtStyle, onEachFeature: (feature, layer) => {

            layer.on({

                mouseover: function (e) { },

                mouseout: function (e) { },

                click: function (e) { },
            });
        }
    }).addTo(map);

    /* getHospitals on that district */
    $.each(hospitals, function (index, value) {

        let popupText = "".concat("<div class=\"popup\">", value.name, "<br>Patients: ", value.patients, "<br>Free Beds: ", value.freeBeds, "</div>");

        markers.push(L.marker(value.location, { icon: value.freeBeds - value.patients < 10 ? redMarkerIcon : blueMarkerIcon }).addTo(map).bindPopup(popupText));
    })

}

function random(min, max) { 
    
    return Math.floor(Math.random() * max) + min 
}

function getGeoJson() {

    $.get(urlStateJson, function (res) {

        geoData = res;

        //var t = geoData.features.map (ele => { return { name: ele.properties.DISTRICT, healthCentres: random(10, 30), patients: random(20, 200), freeBeds: random (100, 300 ) } }  );

        //console.log (JSON.stringify(t));

        if (geojson) geojson.clearLayers();

        if (titleLayer) map.removeLayer(titleLayer);

        map.fitBounds(stateBounds);

        geojson = L.geoJson(geoData, {

            style: stateStyle, onEachFeature: (feature, layer) => {

                layer.on({

                    mouseover: onMouseOverDistrict,

                    mouseout: onMouseOutDistrict,

                    click: onClickDistrict,
                });
            }
        }).addTo(map);

    });
}

function resetAll() {

    clearMarkers();

    getGeoJson();
}


$("#ak-reset").on('click', () => resetAll());

$(function () {

    console.log(stateData.map ( ele => ele.name));

    resetAll();

});





