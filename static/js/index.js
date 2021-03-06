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

    // to upper case all first letter in a sentence
    function toTitleCase(str){
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

    function validateKeyword(keyword){
        if(keyword == "" || keyword.length < 3){
            $("#keyword-helper").text("Please input at least 3 characters.");
            return false;
        }
        else{
            var regex = /^([a-zA-Z][a-zA-Z0-9]+|#[a-zA-Z]+[a-zA-Z0-9]*)$/g
            if(regex.test(keyword)){
                return true;
            }
            else{
                $("#keyword-helper").text("Incorrect syntax.");
                return false;
            }
        }
    }

    function drawMarkersMap(frequencies){
        var tabledata = [['Province', 'Reproduction Ratio', 'Possible Infected']];
        for (var i = 0; i < frequencies.length; i++){
            if(frequencies[i]['province'] ==  "ncr"){
                tabledata.push(["National Capital Region", parseFloat(frequencies[i]['ratio'].toFixed(4)), Math.round(frequencies[i]['infected'])])
            }
            else{
                tabledata.push([toTitleCase(frequencies[i]['province']), parseFloat(frequencies[i]['ratio'].toFixed(4)), Math.round(frequencies[i]['infected'])])
            }
        }
        var data = google.visualization.arrayToDataTable(tabledata);
        var options = {
            region: 'PH',
            displayMode: 'markers',
            backgroundColor: '#B2D0FE',
            width: '800px',
            colorAxis: {colors: ['green', 'red']}
        }

        var chart = new google.visualization.GeoChart(document.getElementById('geomap-canvas'));
        chart.draw(data, options);
    }

    function get_frequency(word, days){
        $("#loading-details").text("Preparing Map...");
        $("#loader-wrapper").fadeIn();
        var jqxhr = $.get('/homepage/get_tweet_frequency/', {'keyword' : word, 'count' : days}, function(data){
            frequencies = data;
        }, "json")
        .done(function() {
            console.log('success!');
            console.log(frequencies);
            drawMarkersMap(frequencies);
            $("#loader-wrapper").fadeOut();
        })
    }

    function predict(){
        $("#loader-wrapper").fadeOut();
        $("#predict-button").click(function(){
            console.log("predict button clicked");
            var word = $('#search-field').val();
            var days = parseInt($('#days-choices').val());
            get_frequency(word, days);
            $("#geochart-div").show();
            $('html,body').animate({
                scrollTop: $("#geochart-div").offset().top},
                'slow');
            $("#view-stats-div").show();
        });
    };

    function map_tweets(tweets){
        $("#loading-details").text("Plotting Tweets...");
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
        $("#loading-details").text("Retrieving tweets...");
        $("#loader-wrapper").fadeIn();
        var jqxhr = $.get('/homepage/search_keyword/', {keyword: word}, function(data){
            tweets = data;
        })
        .done(function() {
            console.log('success!');
            map_tweets(tweets);
            $("#prediction-option-div").show();
            $("#stats-province-choices").hide();
            $("#loader-wrapper").fadeOut();
        })
    }

	$("#search-button").click(function(){
        var word = $('#search-field').val();
        if(validateKeyword(word)){
            console.log("form submitted");
            $("#ph-stats-link").attr('href', "/homepage/country-stats/" + word +"/");
            get_tweets(word);
            $("#search-div").hide();
            $(".keyword-span").text(word);
            $("#keyword-div").show();
        }
        else{
            $("search-field").val("");
        }
	});

    $("#province-stats-button").click(function(){
        $("#country-stats-button").hide();
        $("#region-stats-button").hide();
        $("#stats-province-choices").show();
        for (var i = 0; i < frequencies.length; i++) {
            var str = frequencies[i]['province'].toLowerCase();
            /*$("#stats-province-choices").append("<option><a href='/homepage/province-stats/"+ str + "/>" + $('#search-field').val() + "/'>" + frequencies[i]['province'] + "</a></option>");*/
            if(frequencies[i]['province'] == "ncr")
                $("#stats-province-choices").append("<option value='/homepage/province-stats/"+ str + "/" + $('#search-field').val() +"/'>" + frequencies[i]['province'].toUpperCase() + "</option>");
            else
                $("#stats-province-choices").append("<option value='/homepage/province-stats/"+ str + "/" + $('#search-field').val() +"/'>" + toTitleCase(frequencies[i]['province']) + "</option>");
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
                if(regions[i]['region'] == "ncr" || regions[i]['region'] == "armm" || regions[i]['region'] == "car")
                    $("#stats-region-choices").append("<option value='/homepage/region-stats/"+ str + "/" + $('#search-field').val() +"/'>" + regions[i]['region'].toUpperCase() + "</option>");
                else
                    $("#stats-region-choices").append("<option value='/homepage/region-stats/"+ str + "/" + $('#search-field').val() +"/'>" + toTitleCase(regions[i]['region']) + "</option>");
            };
        })
    });

    $(".item-span").click(function(){
        var str = $(this).text();
        $("#search-field").val(str);
        $("#search-button").click();
    });

    google.setOnLoadCallback(predict);
});
