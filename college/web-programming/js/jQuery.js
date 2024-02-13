// https://api.jquery.com/jQuery.ajax/

const TIME_API_URL = 'http://worldtimeapi.org/api/';
const WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast';


$(document).ready(function() {
	var jqxhr = $.ajax( "example.php" )
		.done(function() {
			console.log( "success" );
		})
		.fail(function() {
			console.log( "error" );
		})
		.always(function() {
			console.log( "complete" );
		});
		
	$("#getWeather").on('click', getWeather);
	$("#getPosition").on('click', getPosition);
	 	

	$.ajax({
		method: 'GET',
		url: TIME_API_URL + 'timezone',
		data: {
			test: 22
		},
		dataType: 'json',
		timeout: 1000,
		success: function (data) {
			let result = ''
			data.forEach(row => result += `<a href="${row}">${row}</a><br>`);
			// data.forEach(row => result += '<a href="' + row + '>' + row + '</a>');
			$("#content").html(result);
			$("#content a").on('click', LoadTime);
		},
		error: function (error) {
			console.info('timeout: %O', error);
		}
	});
});

function LoadTime(event)
{
	var timeZone = event.target.getAttribute('href');
	LoadTimeByTimeZone(timeZone, LoadTimeCallback);
	return false;
}

function LoadTimeCallback(data)
{
	console.info(data);
	let result = ''
	
	for (const [key, value] of Object.entries(data)) {
		result += (`<b>${key}</b>: ${value}<br>`);
	}
	
	for (var key in data) {
		result += (`<b>${key}</b>: ${data[key]}<br>`);
	}
	$("#content").html(result);
}

function LoadTimeByTimeZone(timeZone, callback)
{
	$.ajax({
		method: 'GET',
		url: TIME_API_URL + 'timezone/' + timeZone,
		dataType: 'json',
		timeout: 5000,
		success: function (data) {
			callback(data);
			return data;
		},
		error: function (error) {
			return [];
		}
	});
}

function getWeather()
{
	$.ajax({
		method: 'GET',
		url: WEATHER_API_URL,
		data: $("#settingsForm").serialize(),
		// data: {
		// 	latitude: $('#latitude').val(),
		// 	longitude: $('#longitude').val(),
		// 	hourly: 'temperature_2m,relative_humidity_2m,rain,cloud_cover,wind_speed_10m',
		// 	wind_speed_unit: 'ms',
		// },
		dataType: 'json',
		timeout: 5000,
		success: function (data) {
			console.info(data);
		},
		error: function (error) {
			console.error(error);
		}
	});
}

function getPosition()
{
	// https://developer.mozilla.org/ru/docs/Web/API/Geolocation/getCurrentPosition
	var options = {
		enableHighAccuracy: true,
		timeout: 5000,
		maximumAge: 0,
	};
	
	function success(pos) {
		var crd = pos.coords;
		
		console.log("Ваше текущее местоположение:");
		console.log(`Широта: ${crd.latitude}`);
		console.log(`Долгота: ${crd.longitude}`);
		console.log(`Плюс-минус ${crd.accuracy} метров.`);
		
		$('#latitude').val(crd.latitude);
		$('#longitude').val(crd.longitude);
		
	}
	
	function error(err) {
		console.warn(`ERROR(${err.code}): ${err.message}`);
	}
	
	navigator.geolocation.getCurrentPosition(success, error, options);

}