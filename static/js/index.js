google.load('visualization', '1', {'packages': ['geochart']});
$(document).ready(function(){
	var map = new GMaps({
      	div: '#map-canvas',
        lat: 14.5833,
        lng: 120.9667,
        width: '700px',
        height: '700px',
        zoom: 6,
        zoomControl: true,
        zoomControlOpt: {
            style: 'SMALL',
            position: 'TOP_LEFT'
        },
        panControl: false
    });

   
    function map_tweets(tweets){
        console.log(tweets);
        for (var i = 0; i < tweets.length; i++) {
            map.addMarker({
                lat: tweets[i].fields['lat'],
                lng: tweets[i].fields['lon'],
                title: tweets[i].fields['tweetId']
            });
        };
    };

    function drawMarkersMap(frequencies){
        var tabledata = [['Province',   'Population']];
        for (var i = 0; i < frequencies.length; i++){
            if(frequencies[i]['province'] ==  "NCR")
                tabledata.push(["National Capital Region", frequencies[i]['infected']])
            else
                tabledata.push([frequencies[i]['province'], frequencies[i]['infected']])
        }
        var data = google.visualization.arrayToDataTable(tabledata);
        var options = {
            region: 'PH',
            displayMode: 'markers',
            backgroundColor: '#B2D0FE',
            colorAxis: {colors: ['green', 'red']}
        }

        var chart = new google.visualization.GeoChart(document.getElementById('geomap-canvas'));
        chart.draw(data, options);
    }

    function predict(){
        $("#test-button").click(function(){
            console.log("test button clicked");
            var word = $('#search-field').val();
            get_frequency(word);    
        });
    };

    function get_tweets(word){
        var jqxhr = $.get('/homepage/search_keyword/', {keyword: word}, function(data){
            tweets = data;
        })
        .done(function() {
            console.log('success!');
            map_tweets(tweets);
        })
    }

	$("#search-button").click(function(){
		console.log("form submitted");
        var word = $('#search-field').val();
        get_tweets(word);
	});

    function get_frequency(word){
        var jqxhr = $.get('/homepage/get_tweet_frequency/', {keyword: word}, function(data){
            frequencies = data;
        })
        .done(function() {
            console.log('success!');
            console.log(frequencies);
            drawMarkersMap(frequencies);
        })
    }

    google.setOnLoadCallback(predict);
});
