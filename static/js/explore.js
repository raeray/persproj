var map = L.map('map').setView([33.3216322198, -111.9625568958], 17)    

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: 'OSM'
}).addTo(map)


var starChartElement = document.getElementById('starChart');
var starChart = new Chart(starChartElement, {
type: 'bar',
data: {
	labels: ['1', '1.5', '2','2.5', '3','3.5', '4','4.5', '5'],
	datasets: [{
		label: '# of Restaurants',
		data: [0, 0, 0, 0, 0, 0, 0, 0, 0],
		// data: [business_1_stars,business_15_stars,business_2_stars,business_25_stars,business_3_stars,business_35_stars,business_4_stars,business_45_stars,business_5_stars],
		backgroundColor: [
			'rgba(255, 99, 132, 0.2)',
			'rgba(255, 99, 132, 0.2)',
			'rgba(54, 162, 235, 0.2)',
			'rgba(54, 162, 235, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(75, 192, 192, 0.2)',
			'rgba(75, 192, 192, 0.2)',
			'rgba(153, 102, 255, 0.2)'
			],
		borderColor: [
			'rgba(255, 99, 132, 1)',
			'rgba(255, 99, 132, 1)',
			'rgba(54, 162, 235, 1)',
			'rgba(54, 162, 235, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(75, 192, 192, 1)',
			'rgba(75, 192, 192, 1)',
			'rgba(153, 102, 255, 1)'
		],
		borderWidth: 1
	}]
},
options: {
	scales: {
		yAxes: [{
			ticks: {
				beginAtZero: true
			}
		}]
	}
}
});

var topicChartElement = document.getElementById('topicChart');
var topicChart = new Chart(topicChartElement, {
type: 'bar',
data: {
	labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
	datasets: [{
		label: 'Average among Reviews',
		data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		// data: [business_1_stars,business_15_stars,business_2_stars,business_25_stars,business_3_stars,business_35_stars,business_4_stars,business_45_stars,business_5_stars],
		backgroundColor: [
			'rgba(255, 99, 132, 0.2)',
			'rgba(255, 99, 132, 0.2)',
			'rgba(54, 162, 235, 0.2)',
			'rgba(54, 162, 235, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(75, 192, 192, 0.2)',
			'rgba(75, 192, 192, 0.2)',
			'rgba(153, 102, 255, 0.2)',
			'rgba(153, 102, 255, 0.2)',
			'rgba(153, 102, 255, 0.2)',
			'rgba(153, 102, 255, 0.2)',
			'rgba(153, 102, 255, 0.2)'
			],
		borderColor: [
			'rgba(255, 99, 132, 1)',
			'rgba(255, 99, 132, 1)',
			'rgba(54, 162, 235, 1)',
			'rgba(54, 162, 235, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(75, 192, 192, 1)',
			'rgba(75, 192, 192, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(153, 102, 255, 1)'
		],
		borderWidth: 1
	}]
},
options: {
	scales: {
		yAxes: [{
			ticks: {
				beginAtZero: true
			}
		}]
	}
}
});


var greenIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var blueIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});
var yellowIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});
var orangeIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});
var redIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [25, 41],
	iconAnchor: [12, 41],
	popupAnchor: [1, -34],
	shadowSize: [41, 41]
});

var markers = new L.LayerGroup();

var business_5_stars = {value: 0};
var business_45_stars = {value: 0};
var business_4_stars = {value: 0};
var business_35_stars = {value: 0};
var business_3_stars = {value: 0};
var business_25_stars = {value: 0};
var business_2_stars = {value: 0};
var business_15_stars = {value: 0};
var business_1_stars = {value: 0};


var business_list = [
business_1_stars,
business_15_stars,
business_2_stars,
business_25_stars,
business_3_stars,
business_35_stars,
business_4_stars,
business_45_stars,
business_5_stars
]

// used for saving restaurant info
var reviews_list;

function getBounds() {

	removeData(starChart);
	
	var bounds = map.getBounds();
	var business_id_list = [];

	axios.get('http://127.0.0.1:5000/business_geo', {params: {boundaries: bounds}})
	.then(response => {

		// add businesses to the map
		
		L.geoJSON(response.data, {pointToLayer: function(feature, latlng) {
			switch (feature.business_stars) {
				case 5.0:
					business_list[8].value += 1
					marker =  L.marker(latlng, {icon: greenIcon})
					markers.addLayer(marker);
					return marker;
				case 4.5:
					business_list[7].value += 1
					marker =  L.marker(latlng, {icon: blueIcon})
					markers.addLayer(marker);
				case 4.0: 
					business_list[6].value += 1
					marker =  L.marker(latlng, {icon: blueIcon})
					markers.addLayer(marker);
					return marker;
				case 3.5:
					business_list[5].value += 1
					marker =  L.marker(latlng, {icon: yellowIcon})
					markers.addLayer(marker);
					return marker; 
				case 3.0:
					business_list[4].value += 1
					marker =  L.marker(latlng, {icon: yellowIcon})
					markers.addLayer(marker);
					return marker; 
				case 2.5: 
					business_list[3].value += 1
					marker =  L.marker(latlng, {icon: orangeIcon})
					markers.addLayer(marker);
					return marker; 
				case 2.0: 
					business_list[2].value += 1
					marker =  L.marker(latlng, {icon: orangeIcon})
					markers.addLayer(marker);
					return marker;
				case 1.5: 
					business_list[1].value += 1
					marker =  L.marker(latlng, {icon: redIcon})
					markers.addLayer(marker);
					return marker; 
				case 1.0: 
					business_list[0].value += 1
					marker =  L.marker(latlng, {icon: redIcon})
					markers.addLayer(marker);
					return marker; 
				default:
					marker =  L.marker(latlng, {icon: yellowIcon})
					markers.addLayer(marker);
					return marker; 
			}
		}
		, onEachFeature: onEachFeature}
		).addTo(map);

	addData(starChart, business_list.map(function (x) {return x.value}))

	})
	
};


// load datatabel when javascript is readu
 $(document).ready(function() {
	$('#review_table').DataTable({
		'dom':'<"c8tableTools01"Bf><"c8tableBody"t><"c8tableTools02"lipr>',
		"pageLength" : 3,
		"deferRender": true,
		// "scroller":true,
		// "scrollY": "500px",
		// "scrollCollapse": true,
		// "fixedColumns": true,
		// "data": reviews_list,
		"columns": [
			{"data" :'date'},
			{"data" :'text'},
			{"data" :'review_stars'},
			{"data" :'cool'},
			{"data" :'funny'},
			{"data" :'useful'},
			{"data" :'reviewId'}
		],
		"columnDefs": [
		 	{
		 		render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-600'>" + data + "</div>";
               	}
                , "targets": 1 }
			]
		});

	$('#review_table').DataTable().draw()
}
)


function onEachFeature(feature, layer) {
	message = String(feature.name) + "<br>review count: " + String(feature.review_count)
	+ "<br>business stars: " + String(feature.business_stars)

	layer.on('click', function onClick() {

		removeData(topicChart)
		
		// reset review list
		var reviews_list = '';

		// call the review api to get all the reviews for business id
		axios
		.get('http://127.0.0.1:5000/review', {params: {business_id: feature.business_id}})
		.then(response => {

		reviews_list = response.data;

		// clear previous data
		$('#review_table').DataTable().clear()
		// show reviews on table
		setupData(reviews_list)

		// call topics and get topic distribution 
		axios.get('http://127.0.0.1:5000/topics', {params: {review_list: reviews_list}})
		.then(response => {
			console.log('calls new api on js',response.data)
			// topic list
			topic_list = response.data;
			addData(topicChart, topic_list);
		});

		
		});

		
	});
	layer.bindPopup(message);
};

function setupData(reviews_list) {
	
	$(document).ready(function() {
		// add new data and draw
		$('#review_table').DataTable().rows.add(reviews_list).draw()
	})


	};


function clearLayers() {

	removeData()

	for (i=0;i<business_list.length; i ++) {
		business_list[i].value = 0
	}

	map.removeLayer(markers)
	var markers = new L.LayerGroup();
}

function deleteAllMarkers() {

	$.each(map._layers, function (ml) {

		if (map._layers[ml].feature) {
			console.log(this)
			map.removeLayer(this)
		}
	})

}


function addData(chart, input_data) {

	chart.data.datasets[0].data = input_data
	chart.update();
}

function removeData(chart) {
	
	chart.data.datasets[0].data = []
	// for (i=0;i<business_list.length; i ++) {
	// 	business_list[i].value = 0
	// }
	// chart.data.labels.pop();
	chart.data.datasets.forEach((dataset) => {
		dataset.data.pop();
	});

	chart.update();

}

		
// 	}})
	
	

// 	// console.log('updated values outside', business_list.map(function (x) {return x.value}))
// })
// }