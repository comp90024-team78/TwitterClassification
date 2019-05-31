

function drawPieChart() {

    var data = google.visualization.arrayToDataTable([
      ['Sins', 'People Count'],
      ['Lust',     11],
      ['Gluttony',      8],
      ['Greed',  6],
      ['Sloth', 2],
      ['Wrath',    7],
      ['Envy',    9],
      ['Pride',    5]
    ]);



    var options = {
      title: '7 Deadly Sins',
      titlePosition: 'none',
chartArea: {width: '90%', height: '80%'}
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}


function drawBarChart() {
      var data = google.visualization.arrayToDataTable([
        ["Sins", "People Count", { role: "style" } ],
        ["Lust", 11, "#b87333"],
        ["Gluttony", 8, "silver"],
        ["Greed", 6, "gold"],
        ["Sloth", 2, "color: #e5e4e2"],
        ["Wrath", 7, "color: #a7e4e2"],
        ["Envy", 9, "color: #f5e4e2"],
        ["Pride", 5, "color: #c5e4e2"]
      ]);

      var view = new google.visualization.DataView(data);
      view.setColumns([0, 1,
                       { calc: "stringify",
                         sourceColumn: 1,
                         type: "string",
                         role: "annotation" },
                       2]);

      var options = {
        title: '7 Deadly Sins',
        titlePosition: 'none',
        width: 600,
        height: 300,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
      };
      var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
      chart.draw(view, options);
}

function drawLineChart() {
        var data = google.visualization.arrayToDataTable([
          ['Sins', 'People Count'],
          ['Lust',  1000],
          ['Gluttony',  1170],
          ['Greed',  660],
          ['Sloth',  1030],
          ['Wrath',  1030],
          ['Envy',  1030],
          ['Pride',  1030]
        ]);

        var options = {
          title: '7 Deadly Sins',
          titlePosition: 'none',
          curveType: 'function',
          width: 800,
          height: 400,
          legend: { position: 'bottom' },
          chartArea: {width: '90%', height: '80%'}
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
}

