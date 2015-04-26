google.load('visualization', '1.1', {packages: ['line', 'corechart']});
$(document).ready(function(){
google.setOnLoadCallback(show_stats);
  var keyword = $("#keyword-span").text();
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
    rows.push(['Province', 'Population', 'Frequency']);
    for (var i = 0; i < freq_per_province.length; i++) {
      var temp = [];
      temp.push(freq_per_province[i]['province']);
      temp.push(freq_per_province[i]['population']);
      temp.push(freq_per_province[i]['frequency']);
      rows.push(temp);
    };
    var data2 = google.visualization.arrayToDataTable(rows);

    var options2 = {
      title: 'Correlation between life expectancy, fertility rate and population of some world countries (2010)',
      hAxis: {title: 'Population'},
      vAxis: {title: 'Frequency'},
      bubble: {textStyle: {fontSize: 11}},
      width: 800,
      height: 500,
    };

    var chart2 = new google.visualization.BubbleChart(document.getElementById('country-bubble-div'));
    chart2.draw(data2, options2);
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