google.load('visualization', '1.1', {packages: ['corechart']});
$(document).ready(function(){
    google.setOnLoadCallback(show_stats);

    function toTitleCase(str){
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }

    var keyword = $("#keyword-span").text();
    $("#keyword-span").text(toTitleCase(keyword));
    var province = $("#province-span").text();
    $("#province-span").text(toTitleCase(province));
    
    function drawLineChart(freq_per_day){
        var rows = [];
        rows.push(['Date', 'Frequency']);
        var totalTweets = 0;
        
        // add data to table for visalization
        for (var i = 0; i < freq_per_day.length -1; i++) {
            var temp = [];
            temp.push(freq_per_day[i]['date']);
            temp.push(freq_per_day[i]['frequency']);
            totalTweets += freq_per_day[i]['frequency'];
            rows.push(temp);
        };
        
        // for tweet count
        $("#tweet-count-span").text(totalTweets);
        $("#tweet-number-div div div").first().append("<span class='glyphicon glyphicon-retweet'></span>");
        
        // for day rate
        var dayIncrease = ((freq_per_day[freq_per_day.length -2]['frequency'] - freq_per_day[freq_per_day.length -3]['frequency'])/freq_per_day[freq_per_day.length -3]['frequency']) * 100;
        var str = '';
        if(dayIncrease >= 0){
            str = "<span class='glyphicon glyphicon-arrow-up'></span>";
        }
        else{
            if(isNaN(dayIncrease) || !isFinite(dayIncrease))
                dayIncrease = 0;
            str = "<span class='glyphicon glyphicon-arrow-down'></span>";
        }
        $("#day-rate-span").text(Math.abs(dayIncrease).toFixed(0) + "%");
        $("#day-rate-div div div").first().append(str);
        
        // for week rate
        var weekIncrease = ((freq_per_day[freq_per_day.length -2]['frequency'] - freq_per_day[0]['frequency'])/freq_per_day[0]['frequency']) * 100;
        if(weekIncrease >= 0){
            str = "<span class='glyphicon glyphicon-arrow-up'></span>";
        }
        else{
            if(isNaN(weekIncrease) || !isFinite(weekIncrease))
                weekIncrease = 0;
            str = "<span class='glyphicon glyphicon-arrow-down'></span>";
        }
        $("#week-rate-span").text(Math.abs(weekIncrease).toFixed(0) + "%");
        $("#weekly-rate-div div div").first().append(str);
        
        // for rank
        $("#rank-span").text(freq_per_day[freq_per_day.length - 1]['rank'])

        // options for bar garph
        var options = {
            title: 'Frequency per day',
            width: 800,
            height: 500,
            legend: 'none',
            hAxis: {title: 'date'},
            vAxis: {title: 'frequency'}
        }

        var data = google.visualization.arrayToDataTable(rows);
        var chart = new google.visualization.ColumnChart(document.getElementById('province-chart-div'));
        chart.draw(data, options);
        $("#loader-wrapper").fadeOut();
    }

    // ajax for getting frequency and rank
    function show_stats(){
        var jqxhr = $.get('/homepage/daily_province_stats/', {'keyword' : keyword, 'province' : province}, function(data){
            freq_per_day = data;
            }, "json")
        .done(function() {
            console.log('success!');
            console.log(freq_per_day);
            drawLineChart(freq_per_day);
        })
    }

});