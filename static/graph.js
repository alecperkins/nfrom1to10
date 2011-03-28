(function() {
  var data, data_url, drawGraphs, generated, getData, i, init, overall_data;
  data_url = "/data/";
  data = {};
  overall_data = (function() {
    var _results;
    _results = [];
    for (i = 1; i <= 10; i++) {
      _results.push([i, 0]);
    }
    return _results;
  })();
  generated = null;
  getData = function() {
    return $.getJSON(data_url, {}, function(response) {
      data = response;
      return drawGraphs();
    });
  };
  drawGraphs = function() {
    var graph_boxes, graph_data, graph_opts, i, method, overall_opts, results, sum;
    $("#spinner").hide();
    graph_boxes = {
      overall: $("#overview-graph"),
      input: $("#input-graph"),
      radio: $("#radio-graph"),
      select: $("#select-graph"),
      slider: $("#slider-graph")
    };
    $("#graphs").show();
    generated = new Date(data.input.generated);
    sum = 0;
    for (method in data) {
      results = data[method];
      for (i = 1; i <= 10; i++) {
        overall_data[i - 1][1] += results.data[i - 1];
        sum += results.data[i - 1];
      }
      graph_data = (function() {
        var _results;
        _results = [];
        for (i = 1; i <= 10; i++) {
          _results.push([i, results.data[i - 1]]);
        }
        return _results;
      })();
      graph_opts = {
        bars: {
          show: true,
          align: "center"
        },
        data: graph_data
      };
      $.plot(graph_boxes[method], [graph_opts]);
    }
    overall_opts = {
      bars: {
        show: true,
        align: "center"
      },
      data: overall_data
    };
    $.plot(graph_boxes.overall, [overall_opts]);
    return $("#as-of").html("For now, here's a preliminary breakdown as of <strong>" + (generated.toGMTString()) + "</strong><br>Total votes: <strong>" + sum + "</strong>");
  };
  init = function() {
    return getData();
  };
  $(document).ready(init);
}).call(this);
