$(document).ready(function(){
	var map = new GMaps({
      	div: '#map-canvas',
        lat: 14.5833,
        lng: 120.9667,
        width: '700px',
        height: '700px',
        zoom: 5,
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
                title: tweets[i].fields['tweetId'],
            });
        };
    }

	$("#search-button").click(function(){
		console.log("form submitted");
        tweets = '';
		var jqxhr = $.get('/homepage/search_keyword/', {keyword: $('#search-field').val()}, function(data){
			tweets = data;
			/*for (var tweet in tweets){
				console.log(tweet.user + " : " + tweet.text);
			}*/
    	})
    	.done(function() {
            console.log('success!');
            map_tweets(tweets);
		})
	});
});
