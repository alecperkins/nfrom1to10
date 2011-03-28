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
    var graph_boxes, graph_data, graph_opts, i, label, method, overall_opts, random_specified, res, results, sum, _i, _len, _ref;
    $("#spinner").hide();
    graph_boxes = {
      overall: $("#overview-graph"),
      input: $("#input-graph"),
      radio: $("#radio-graph"),
      select: $("#select-graph"),
      slider: $("#slider-graph")
    };
    $("#graphs").show();
    generated = data.input.random_not_specified.generated;
    sum = 0;
    for (method in data) {
      results = data[method];
      graph_opts = [];
      _ref = ["random_specified", "random_not_specified"];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        random_specified = _ref[_i];
        res = results[random_specified];
        label = random_specified.replace(/_/g, " ");
        for (i = 1; i <= 10; i++) {
          overall_data[i - 1][1] += res.data[i - 1];
          sum += res.data[i - 1];
        }
        graph_data = (function() {
          var _results;
          _results = [];
          for (i = 1; i <= 10; i++) {
            _results.push([i, res.data[i - 1]]);
          }
          return _results;
        })();
        graph_opts.push({
          label: label,
          bars: {
            show: true,
            align: "center",
            barwidth: 0.1
          },
          data: graph_data
        });
      }
      $.plot(graph_boxes[method], graph_opts);
    }
    overall_opts = {
      bars: {
        show: true,
        align: "center"
      },
      data: overall_data
    };
    $.plot(graph_boxes.overall, [overall_opts]);
    return $("#as-of").html("For now, here's a preliminary breakdown as of <strong>" + generated + "</strong><br>Total votes: <strong>" + sum + "</strong>");
  };
  init = function() {
    return getData();
  };
  $(document).ready(init);
}).call(this);
