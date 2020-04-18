/* configuration */

let apiHost = "http://localhost:8000";

let geoJsonPath = "/static/geojson/";

blueMarkerIconUrl = "/static/images/marker-icon.png";

redMarkerIconUrl = "/static/images/marker-icon-red.png";

let stateName = null;

let endpoints = {
	totalcounts: "/assetmgt/totalcounts",
    state: "/assetmgt/getstatedata",
    district: "/assetmgt/getdistrictdata",
    statedetails:"/assetmgt/getstatenamebyid"
};

/*  end of configuration */

let defaultZoom = 7;

let stateCenter = null;

let stateCenters = {

    Kerala: [10.808036, 76.305992],

    Meghalaya: [25.579659, 91.319157],

    Puducherry: [11.940408, 79.815845],

    Ladakh: [34.223132, 77.475905],

    TamilNadu: [10.985378, 78.664046]
};

let stateBounds = [
    [14.314431, 81.331526],
    [8.063881, 76.314360]
];

let isDistrictSelected = false;

let stateData = null;

let assetsList = null;

let markers = [];

let urlStateJson = null;

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
});

let info = L.control();

info.onAdd = function (map) {

    this._div = L.DomUtil.create('div', 'info');

    this.updateForDistrict();

    return this._div;
};

info.updateForDistrict = function (properties) {

    let dist;

    if (properties) {

        dist = stateData.filter(ele => ele.district == properties.DISTRICT)

        if (dist.length) dist[0].info.freeBeds - dist[0].info.patients < 10 ? this._div.classList.add('ak-alert') : this._div.classList.remove('ak-alert');
    }

    this._div.innerHTML = (properties && dist.length ?
        "".concat(
            '<h4>', properties.DISTRICT, '</h4>',
            "Health Centres: ", dist[0].info.healthcentres,
            ", Patients: ", dist[0].info.patients,
            ", Free Beds: ", dist[0].info.freebeds
        ) : 'Hover over a district');
}

info.addTo(map);

function stateStyle(feature) {

    let patientsCount = 0;

    // console.log (feature.properties.DISTRICT);
    let selState = stateData.filter(ele => ele.district == feature.properties.DISTRICT);

    if (selState.length) {

        patientsCount = selState[0].info.patients
    }
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

    // console.log(layer.feature.properties.DISTRICT)

    info.updateForDistrict(layer.feature.properties);
}

function onMouseOutDistrict(e) {

    geojson.resetStyle(e.target);
}

function onClickDistrict(e) {

    isDistrictSelected = true;

    let selectedDistrict = e.target.feature.properties.DISTRICT;

    console.log(selectedDistrict);

    // titleLayer = L.tileLayer.wms('https://bhuvan-vec1.nrsc.gov.in/bhuvan/gwc/service/wms?', {layers: 'indiainf',maxZoom: 18 }).addTo(map);
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
    $.get(apiHost.concat(endpoints.district), { q: selectedDistrict }, function (res) {
        // $.get("/static/data/karthi/district.json", { q: selectedDistrict }, function (res) {

        districtData = res;

        console.log(districtData);
        /* Generate markers for the district */
        $.each(districtData, function (index, value) {

            console.log(value.location, isNaN(parseFloat(value.location[0])), isNaN(parseFloat(value.location[1])));

            if (!
                (
                    isNaN(parseFloat(value.location[0])) &&

                    isNaN(parseFloat(value.location[1]))
                )
            ) {

                let hKeys = Object.keys(value.assets);

                let popUpBalance = "";

                hKeys.forEach(function (hKey) {

                    popUpBalance += hKey + ': ' + value.assets[hKey].free + '<br>';
                });

                let popupText = "".concat("<div class=\"popup\">", value.name, "<br>Patients: ", value.patients, "<br>", popUpBalance, "</div>");


                markers.push(L.marker(value.location, { icon: blueMarkerIcon }).addTo(map).bindPopup(popupText));
            }
        });

        assetSelectorForDistrictOnChange(assetsList[0]);

        $("#assets-selector").prop('selectedIndex', 0);

    });
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

function addStringArrayToSelect(selectId, stringArray) {

    let options = '';

    for (let i = 0; i < stringArray.length; i++) {

        options += '<option value="' + stringArray[i] + '">' + stringArray[i] + '</option>';
    }
    //$(selectId).prepend("<option value='' selected='selected' disabled>Select</option>");

    $(selectId).append(options);
}

function generateAssetsList(data) {

    assetsList = Object.keys(data.reduce(function (result, obj) {

        return Object.assign(result, obj.assets);

    }, {}));

    addStringArrayToSelect('#assets-selector', assetsList);

    return assetsList;
}

function assetSelectorForStateOnChange(value) {

    console.log(value);

    let selectedAsset = value;

    let districts = stateData.map(ele => ele.district);

    let occupied = stateData.map(ele => ele.assets[selectedAsset].occupied);

    let free = stateData.map(ele => ele.assets[selectedAsset].free);

    let unusable = stateData.map(ele => ele.assets[selectedAsset].unusable);

    console.log ( assetsList, occupied, free, unusable );

    updateTrendsChart({

        labels: districts,

        occupied: occupied,

        free: free,

        unusable: unusable
    });
}

function assetSelectorForDistrictOnChange(value) {

    console.log(value);

    let selectedAsset = value;

    let names = districtData.map(ele => ele.name);

    let occupied = stateData.map(ele => ele.assets[selectedAsset].occupied);

    let free = stateData.map(ele => ele.assets[selectedAsset].free);

    let unusable = stateData.map(ele => ele.assets[selectedAsset].unusable);

    console.log ( assetsList, occupied, free, unusable );

    updateTrendsChart({

        labels: names,

        occupied: occupied,

        free: free,

        unusable: unusable
    });

}

$('#assets-selector').on('change', function () {

    if (isDistrictSelected) {

        assetSelectorForDistrictOnChange(this.value);

    } else {

        assetSelectorForStateOnChange(this.value);
    }
});

function getStateDetails(stateId) {

    return new Promise(function (resolve, reject) {

        $.get( apiHost.concat( endpoints.statedetails ), { q: 24 }, function (res) {

            console.log ( res )
    
            resolve(res)
    
        });
    })
}

function resetAll() {

    console.log ('resetAll')

    isDistrictSelected = false;

    $('#assets-selector').empty();

    clearMarkers();

    getStateDetails(24).then(function (res) {

        console.log ( res );

        stateName = res.stateName.split(" ").join("");

        console.log ( stateName );

        urlStateJson = geoJsonPath.concat(stateName, ".json");

        stateCenter = stateCenters[stateName];

        map.setView(stateCenter, defaultZoom);

        $.get(apiHost.concat (endpoints.state),{ state: stateName } , function (res) {

            // $.get("/static/data/karthi/state.json", function (res) {

            // console.log(JSON.stringify(res));

            stateData = res;

            console.log ( stateData )

            assetsList = generateAssetsList(stateData);

            console.log ( assetsList )

            assetSelectorForStateOnChange(assetsList[0]);

            $("#assets-selector").prop('selectedIndex', 0);

            getGeoJson();

        });

        $.get(apiHost.concat (endpoints.totalcounts),{ state: stateName } , function (res) {
            // $.get("/static/data/karthi/totalcounts.json", function (res) {

            $('#totalhospitals').html(res.totalhospitals);
            $('#patientsadmitted').html(res.patientsadmitted);
            $('#availablebeds').html(res.availablebeds);
            $('#availableventilators').html(res.availableventilators);
        });

    }).catch  ( function (err){

        console.log ( err );
    })

}

$("#ak-reset").on('click', () => resetAll());

$(function () {

    resetAll();

});





