google.load('visualization', '1.1', {packages: ['line']});
$(document).ready(function(){
google.setOnLoadCallback(show_stats);

  function drawChart(freq_per_day, keyword){
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
          title: 'Philippine Statistics for ' + keyword,
          subtitle: 'in tweets'
        },
        width: 800,
        height: 500
      }

      var chart = new google.charts.Line(document.getElementById('country-chart-div'));

      chart.draw(data, options);
  }

  function show_stats(){
      var keyword = $("#keyword-span").text();
      var jqxhr = $.get('/homepage/get_country_stats/', {'keyword' : keyword}, function(data){
            freq_per_day = data;
        }, "json")
        .done(function() {
            console.log('success!');
            console.log(freq_per_day);
            drawChart(freq_per_day, keyword);
        })
    }
});