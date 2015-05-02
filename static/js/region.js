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
      var endDate = freq_per_day[freq_per_day.length -1]['date'];
      for (var i = 0; i < freq_per_day.length; i++) {
        var temp = [];
        temp.push(freq_per_day[i]['date']);
        temp.push(freq_per_day[i]['frequency']);
        totalTweets += freq_per_day[i]['frequency'];
        rows.push(temp);
      };

      var dayIncrease = ((freq_per_day[freq_per_day.length -1]['frequency'] - freq_per_day[freq_per_day.length -2]['frequency'])/freq_per_day[freq_per_day.length -2]['frequency']) * 100;
      var weekIncrease = 
      $("#tweet-count").text(totalTweets);
      $("#date-range").text(startDate + " - " + endDate);
      if(dayIncrease > 0) var str = "increase";
      else var str = "decrease";
      $("#day-rate").text(Math.abs(dayIncrease).toFixed(2) + " " + str);

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