google.load('visualization', '1.1', {packages: ['line']});
$(document).ready(function(){
google.setOnLoadCallback(show_stats);
  var keyword = $("#keyword-span").text();
  var region = $("#region-span").text();
  function drawLineChart(freq_per_day){
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Date');
      data.addColumn('number', 'Frequency');

      var rows = [];
      var totalTweets = 0;
      var startDate = freq_per_day[0]['date'];
      var endDate = freq_per_day[freq_per_day.length -2]['date'];
      for (var i = 0; i < freq_per_day.length -1; i++) {
        var temp = [];
        temp.push(freq_per_day[i]['date']);
        temp.push(freq_per_day[i]['frequency']);
        totalTweets += freq_per_day[i]['frequency'];
        rows.push(temp);
      };

      var dayIncrease = ((freq_per_day[freq_per_day.length -2]['frequency'] - freq_per_day[freq_per_day.length -3]['frequency'])/freq_per_day[freq_per_day.length -3]['frequency']) * 100;
      $("#tweet-count-span").text(totalTweets);
      $("#tweet-number-div div").first().append("<span class='glyphicon glyphicon-retweet'></span>");
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
      $("#day-rate-div div").first().append(str);
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
      $("#weekly-rate-div div").first().append(str);
      $("#rank-span").text(freq_per_day[freq_per_day.length - 1]['rank'])
      data.addRows(rows);

      var options = {
        chart: {
          title: 'Statistics for ' + keyword + ' in ' + region,
          subtitle: 'in tweets'
        },
        width: 800,
        height: 500
      }

      var chart = new google.charts.Line(document.getElementById('region-chart-div'));

      chart.draw(data, options);
      $("#loader-wrapper").fadeOut();
  }

  function show_stats(){
    var jqxhr = $.get('/homepage/daily_region_stats/', {'keyword' : keyword, 'region' : region}, function(data){
          freq_per_day = data;
      }, "json")
      .done(function() {
          console.log('success!');
          console.log(freq_per_day);
          drawLineChart(freq_per_day);
      })
  }
});