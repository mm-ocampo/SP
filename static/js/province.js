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
      for (var i = 0; i < freq_per_day.length; i++) {
        var temp = [];
        temp.push(freq_per_day[i]['date']);
        temp.push(freq_per_day[i]['frequency']);
        rows.push(temp);
      };

      data.addRows(rows);

      var options = {
        chart: {
          title: 'Statistics for ' + keyword + ' in ' + province,
          subtitle: 'in tweets'
        },
        width: 800,
        height: 500
      }

      var chart = new google.charts.Line(document.getElementById('province-chart-div'));

      chart.draw(data, options);
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