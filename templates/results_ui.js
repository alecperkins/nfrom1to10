(function() {
  var drawGraphs, generated, init, _ref;
    if ((_ref = window.console) != null) {
    _ref;
  } else {
    window.console = {
      log: function() {}
    };
  };
  generated = null;
  drawGraphs = function() {
    var graph_boxes, graph_data, graph_opts, i, label, main_data, method, random_specified, res, results, sum, _i, _len, _ref2, _results;
    main_data = data.ui_breakdown;
    $("#spinner").hide();
    $("#graphs").show();
    graph_boxes = {
      input: $("#input-graph"),
      radio: $("#radio-graph"),
      select: $("#select-graph"),
      slider: $("#slider-graph")
    };
    generated = main_data.input.random_not_specified.generated;
    sum = 0;
    _results = [];
    for (method in main_data) {
      results = main_data[method];
      graph_opts = [];
      _ref2 = ["random_specified", "random_not_specified"];
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        random_specified = _ref2[_i];
        res = results[random_specified];
        label = random_specified.replace(/_/g, " ");
        graph_data = (function() {
          var _results2;
          _results2 = [];
          for (i = 1; i <= 10; i++) {
            _results2.push([i, res.data[i - 1]]);
          }
          return _results2;
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
      _results.push($.plot(graph_boxes[method], graph_opts));
    }
    return _results;
  };
  init = function() {
    var method, name, _ref2;
    _ref2 = window.pickers;
    for (name in _ref2) {
      method = _ref2[name];
      (new method($("#" + (name.toLowerCase()) + "-method"))).render();
    }
    $('.method').show();
    return drawGraphs();
  };
  $(document).ready(init);
}).call(this);
