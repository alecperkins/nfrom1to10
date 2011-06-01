(function() {
  var data, data_url, drawGraphs, generated, getData, i, init, overall_data, _ref;
    if ((_ref = window.console) != null) {
    _ref;
  } else {
    window.console = {
      log: function() {}
    };
  };
  data_url = "/data/results";
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
    return $.get(data_url, {}, function(response) {
      data = response;
      return drawGraphs();
    }, "json");
  };
  drawGraphs = function() {
    var cdata, country, country_graph_data, country_graph_settings, d, datas, graph_boxes, graph_data, graph_opts, i, k, label, main_data, method, new_t, num, overall_opts, random_specified, res, results, sum, t_diff, t_end, t_start, ticks, time_data, time_opts, time_settings, v, _i, _len, _ref2, _ref3, _ref4;
    main_data = data.breakdown;
    time_data = data.overtime;
    $("#spinner").hide();
    $("#graphs").show();
    graph_boxes = {
      overall: $("#overview-graph"),
      input: $("#input-graph"),
      radio: $("#radio-graph"),
      select: $("#select-graph"),
      slider: $("#slider-graph"),
      overtime: $("#overtime-graph"),
      country: $("#country-graph")
    };
    generated = main_data.input.random_not_specified.generated;
    sum = 0;
    for (method in main_data) {
      results = main_data[method];
      graph_opts = [];
      _ref2 = ["random_specified", "random_not_specified"];
      for (_i = 0, _len = _ref2.length; _i < _len; _i++) {
        random_specified = _ref2[_i];
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
    time_opts = [];
    ticks = [];
    t_start = 0;
    t_end = 0;
    for (num in time_data) {
      datas = time_data[num];
      t_start = datas[0][0];
      t_end = datas[datas.length - 1][0];
      time_opts.push({
        label: (parseInt(num) + 1).toString(),
        lines: {
          show: true
        },
        data: datas
      });
    }
    t_diff = (t_end - t_start) / 4;
    ticks = [t_start];
    for (i = 1; i <= 4; i++) {
      new_t = t_start + (t_diff * i);
      ticks.push(new_t);
    }
    for (i = 0, _ref3 = ticks.length; 0 <= _ref3 ? i < _ref3 : i > _ref3; 0 <= _ref3 ? i++ : i--) {
      d = new Date(ticks[i] * 1000);
      ticks[i] = [ticks[i], "" + (d.getFullYear()) + "-" + (d.getMonth() + 1) + "-" + (d.getDate()) + " " + (d.getHours()) + ":" + (d.getMinutes())];
    }
    time_settings = {
      xaxis: {
        ticks: ticks
      }
    };
    $.plot(graph_boxes.overtime, time_opts, time_settings);
    country_graph_data = [];
    for (country in country_data) {
      cdata = country_data[country];
      d = [];
      _ref4 = cdata.data;
      for (k in _ref4) {
        v = _ref4[k];
        d.push([parseInt(k), v / cdata.total]);
      }
      country_graph_data.push({
        label: country,
        lines: {
          show: true
        },
        data: d
      });
    }
    country_graph_settings = {
      xaxis: {
        ticks: (function() {
          var _results;
          _results = [];
          for (i = 1; i <= 10; i++) {
            _results.push([i, i]);
          }
          return _results;
        })()
      }
    };
    $.plot(graph_boxes.country, country_graph_data, country_graph_settings);
    return $("#as-of").html("Here's a breakdown as of <strong>" + generated + "</strong><br>Total votes: <strong>" + sum + "</strong>");
  };
  init = function() {
    var method, name, _ref2;
    getData();
    _ref2 = window.pickers;
    for (name in _ref2) {
      method = _ref2[name];
      (new method($("#" + (name.toLowerCase()) + "-method"))).render();
    }
    return $('.method').show();
  };
  $(document).ready(init);
}).call(this);
