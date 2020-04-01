console.log('explore topics js loaded')

// don't forget to include leaflet-heatmap.js


var baseLayer = L.tileLayer(
	'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
	attribution: 'OSM',
	maxZoom: 40
	}
);


var cfg = {
  // radius should be small ONLY if scaleRadius is true (or small radius is intended)
  // if scaleRadius is false it will be the constant radius used in pixels
  "radius": 20,
  "maxOpacity": .8,
  // scales the radius based on map zoom
  // "scaleRadius": true,
  // if set to false the heatmap uses the global maximum for colorization
  // if activated: uses the data maximum within the current map boundaries
  //   (there will always be a red spot with useLocalExtremas true)
  "useLocalExtrema": true,
  // which field name in your data represents the latitude - default "lat"
  latField: 'lat',
  // which field name in your data represents the longitude - default "lng"
  lngField: 'lng',
  // which field name in your data represents the data value - default "value"
  valueField: 'count'
};

var heatmapLayer = new HeatmapOverlay(cfg);

var map = new L.Map('map', {
  center: new L.LatLng(36.102543, -115.169884),
  zoom: 15,
  layers: [baseLayer, heatmapLayer]
});


function search(nameKey, myArray){
	var return_array = []
	for (var i=0; i < myArray.length; i++) {
		return_array.push(myArray[i][nameKey])
	}
	return return_array
}

// axios.get(...)
//   .then((response) => {
//     return axios.get(...); // using response.data
//   })
//   .then((response) => {
//     console.log('Response', response);
//   });

// function calldropdown(dropdownresult) {

// 	getBounds(filter_value)

// }

function getBounds(filter_value) {

	
	var bounds = map.getBounds();
	var business_id_list = [];
	var testData = {
		  max: 40,
		  data: []
		};


	axios.get('http://127.0.0.1:5000/business_geo', {params: {boundaries: bounds}})
	.then(response => {

		

		// get businesses in a certain area
		var business_list = search('business_id',response.data)
		console.log('BUSINESS LIST', business_list)
		// return axios.get('http://127.0.0.1:5000/review_batch', {params: {business_list: business_list}})
		
		// var filter_value = document.getElementById('dropdownresult')
		// get the data of intensity
		var review_topics = axios
		.get('http://127.0.0.1:5000/review_batch', {params: 
			{business_list: business_list,
			filter_value: filter_value
		}});

		return review_topics
		// return review_list

		// return list of review ids
		// return review_list
		}
	)
	.then(response => {

		testData.data = response.data
		heatmapLayer.setData(testData);
		heatmapLayer.addTo(map)
		}
	)
};

