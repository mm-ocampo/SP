google.load('visualization', '1', {'packages': ['geochart']});
$(document).ready(function(){
	var map = new GMaps({
      	div: '#map-canvas',
        lat: 12.5833,
        lng: 121.9667,
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

    function drawMarkersMap(frequencies){
        var tabledata = [['Province', 'Percentage', 'Infected']];
        for (var i = 0; i < frequencies.length; i++){
            if(frequencies[i]['province'] ==  "NCR")
                tabledata.push(["National Capital Region", frequencies[i]['percentage'], frequencies[i]['infected']])
            else
                tabledata.push([frequencies[i]['province'], frequencies[i]['percentage'], frequencies[i]['infected']])
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

    function get_frequency(word, days){
        var jqxhr = $.get('/homepage/get_tweet_frequency/', {'keyword' : word, 'count' : days}, function(data){
            frequencies = data;
        }, "json")
        .done(function() {
            console.log('success!');
            console.log(frequencies);
            drawMarkersMap(frequencies);
        })
    }

    function predict(){
        $("#predict-button").click(function(){
            console.log("predict button clicked");
            var word = $('#search-field').val();
            var days = parseInt($('#days-choices').val());
            get_frequency(word, days);
            $("#view-stats-div").show();
        });
    };

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

    function get_tweets(word){
        var jqxhr = $.get('/homepage/search_keyword/', {keyword: word}, function(data){
            tweets = data;
        })
        .done(function() {
            console.log('success!');
            map_tweets(tweets);
            $("#prediction-option-div").show();
            $("#stats-province-choices").hide();
        })
    }

	$("#search-button").click(function(){
		console.log("form submitted");
        var word = $('#search-field').val();
        $("#ph-stats-link").attr('href', "/homepage/country-stats/" + word +"/");
        get_tweets(word);
	});

    $("#province-stats-button").click(function(){
        $("#country-stats-button").hide();
        $("#region-stats-button").hide();
        $("#stats-province-choices").show();
        for (var i = 0; i < frequencies.length; i++) {
            var str = frequencies[i]['province'].toLowerCase();
            /*$("#stats-province-choices").append("<option><a href='/homepage/province-stats/"+ str + "/>" + $('#search-field').val() + "/'>" + frequencies[i]['province'] + "</a></option>");*/
            $("#stats-province-choices").append("<option value='/homepage/province-stats/"+ str + "/" + $('#search-field').val() +"/'>" + frequencies[i]['province'] + "</option>");
        };   
    });

    $("#region-stats-button").click(function(){
        $("#country-stats-button").hide();
        $("#province-stats-button").hide();
        $("#stats-region-choices").show();
        var jqxhr = $.get('/homepage/get_regions/', {keyword: $('#search-field').val()}, function(data){
            regions = data;
        })
        .done(function() {
            console.log('success!');
            console.log(regions);
            for (var i = 0; i < regions.length; i++) {
                var str = regions[i]['region'].toLowerCase();
                /*$("#stats-province-choices").append("<option><a href='/homepage/province-stats/"+ str + "/>" + $('#search-field').val() + "/'>" + frequencies[i]['province'] + "</a></option>");*/
                $("#stats-region-choices").append("<option value='/homepage/region-stats/"+ str + "/" + $('#search-field').val() +"/'>" + regions[i]['region'] + "</option>");
            };
        })
    });

    google.setOnLoadCallback(predict);
});
