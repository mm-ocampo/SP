google.load('visualization', '1.1', {packages: ['line']});
$(document).ready(function(){
google.setOnLoadCallback(show_stats);
  var keyword = $("#keyword-span").text();
  var province = $("#province-span").text();
  function drawLineChart(freq_per_day){
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Date');
      data.addColumn('number', 'Frequency');

      var rows = [];
      var totalTweets = 0;
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
        str = "<span class='glyphicon glyphicon-arrow-down'></span>";
      }
      $("#day-rate-span").text(Math.abs(dayIncrease).toFixed(2));
      $("#day-rate-div div").first().append(str);
      var weekIncrease = ((freq_per_day[freq_per_day.length -2]['frequency'] - freq_per_day[0]['frequency'])/freq_per_day[0]['frequency']) * 100;
      if(weekIncrease >= 0){
        str = "<span class='glyphicon glyphicon-arrow-up'></span>";
      }
      else{
        str = "<span class='glyphicon glyphicon-arrow-down'></span>";
      }
      $("#week-rate-span").text(Math.abs(dayIncrease).toFixed(2));
      $("#weekly-rate-div div").first().append(str);
      $("#rank-span").text(freq_per_day[freq_per_day.length - 1]['rank'])
      data.addRows(rows);

      var options = {
        chart: {
          title: 'Statistics for ' + keyword + ' in ' + province,
          subtitle: 'in tweets'
        },
        width: 700,
        height: 500
      }

      var chart = new google.charts.Line(document.getElementById('province-chart-div'));

      chart.draw(data, options);
      $("#loader-wrapper").fadeOut();
  }

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