console.log('js search loaded')
// var map = L.map('map').setView([33.3216322198, -111.9625568958], 17)    

// L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
// 	attribution: 'OSM'
// }).addTo(map)


$(document).ready(function() {
	$('#restaurant_table').DataTable({
		// 'dom':'<"c8tableTools01"Bf><"c8tableBody"t><"c8tableTools02"lipr>',
		"pageLength" : 130,
		"deferRender": true,
		// "scroller":true,
		// "scrollY": "500px",
		// "scrollCollapse": true,
		// "fixedColumns": true,
		// "data": restaurant_info,
		"columns": [
			{"data" :'field'},
			{"data" :'value'},
		],
		// "columnDefs": [
	 // 	{
	 // 		render: function (data, type, full, meta) {
//                  return "<div class='text-wrap width-600'>" + data + "</div>";
//             	}
//              , "targets": 1 }
		// ]
	});
});

function runRestaurantSearch(restaurant_name, location_name) {
	console.log('bubububu')
	// var restaurant_name = document.getElementById('restaurant_name').value
	// var location_name = document.getElementById('location_name').value

	axios.get('http://127.0.0.1:5000/business_details', 
		{params: {restaurant_name: restaurant_name,
			restaurant_location: location_name}}
		)
	.then(response => {

		restaurant_info = response.data

		$(document).ready(function() {
			$('#restaurant_table').DataTable().clear();
			$('#restaurant_table').DataTable().rows.add(restaurant_info.data).draw()

		})

	})

}


