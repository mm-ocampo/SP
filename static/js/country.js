google.load('visualization', '1.1', {packages: ['line', 'corechart']});
$(document).ready(function(){
google.setOnLoadCallback(show_stats);
  var keyword = $("#keyword-span").text();
  function drawLineChart(freq_per_day){
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Date');
      data.addColumn('number', 'Frequency');

      var rows = [];
      var total = 0;
      for (var i = 0; i < freq_per_day.length; i++) {
        var temp = [];
        temp.push(freq_per_day[i]['date']);
        temp.push(freq_per_day[i]['frequency']);
        rows.push(temp);
        total += freq_per_day[i]['frequency'];
      };

      $("#tweet-count-span").text(total);
      $("#tweet-number-div div").first().append("<span class='glyphicon glyphicon-retweet'></span>");
      var dayIncrease = ((freq_per_day[freq_per_day.length -1]['frequency'] - freq_per_day[freq_per_day.length -2]['frequency'])/freq_per_day[freq_per_day.length -2]['frequency']) * 100;
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
      var weekIncrease = ((freq_per_day[freq_per_day.length -1]['frequency'] - freq_per_day[0]['frequency'])/freq_per_day[0]['frequency']) * 100;
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
      data.addRows(rows);

      var options = {
        chart: {
          title: 'Philippine Statistics for ' + keyword,
          subtitle: 'in tweets'
        },
        width: 800,
        height: 500,
        legend: { position: 'bottom' }
      }

      var chart = new google.charts.Line(document.getElementById('country-chart-div'));

      chart.draw(data, options);
  }

  function show_stats(){
    var jqxhr = $.get('/homepage/get_country_stats/', {'keyword' : keyword}, function(data){
          freq_per_day = data;
      }, "json")
      .done(function() {
          console.log('success!');
          console.log(freq_per_day);
          drawLineChart(freq_per_day);
          show_per_province();
      })
  }

  function drawBubbleChart(freq_per_province){
    var rows = [];
    rows.push(['Province', 'Frequency']);
    for (var i = 0; i < freq_per_province.length; i++) {
      var temp = [];
      temp.push(freq_per_province[i]['province']);
      /*temp.push(freq_per_province[i]['population']);*/
      temp.push(freq_per_province[i]['frequency']);
      rows.push(temp);
    };
    var data2 = google.visualization.arrayToDataTable(rows);

    var options2 = {
      title: 'Frequencies of Provinces',
      width: 800,
      height: 500,
      
    };

    var chart2 = new google.visualization.ColumnChart(document.getElementById('country-bubble-div'));
    chart2.draw(data2, options2);
    $("#loader-wrapper").fadeOut();
  }

  function show_per_province(){
    var jqxhr = $.get('/homepage/get_provincial_stats/', {'keyword' : keyword}, function(data){
          freq_per_province = data;
      }, "json")
      .done(function() {
          console.log('success!');
          console.log(freq_per_province);
          drawBubbleChart(freq_per_province);
      })
  }
});