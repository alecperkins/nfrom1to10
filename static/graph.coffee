# data = {"input": {"random_not_specified": {"generated": "2011-03-28T15:16:39.813262+0000", "data": [1545, 1954, 2594, 2910, 2656, 2553, 4059, 2497, 1657, 1034]}, "random_specified": {"generated": "2011-03-28T15:16:40.430402+00:00", "data": [1474, 1901, 2690, 2893, 2683, 2520, 3996, 2515, 1728, 957]}}, "radio": {"random_not_specified": {"generated": "2011-03-28T15:16:45.975702+00:00", "data": [1483, 1912, 2615, 3537, 2550, 2910, 4026, 2090, 1510, 1466]}, "random_specified": {"generated": "2011-03-28T15:16:45.865139+00:00", "data": [1533, 1810, 2646, 3568, 2584, 2893, 3917, 2064, 1566, 1377]}}, "select": {"random_not_specified": {"generated": "2011-03-28T15:16:50.071971+00:00", "data": [1307, 1715, 2509, 2813, 2215, 3724, 4428, 2484, 1489, 1421]}, "random_specified": {"generated": "2011-03-28T15:16:49.797533+00:00", "data": [1373, 1668, 2449, 2772, 6492, 3520, 4258, 2542, 1518, 1370]}}, "slider": {"random_not_specified": {"generated": "2011-03-28T15:16:53.625618+00:00", "data": [1806, 1382, 2525, 3645, 2601, 3005, 3692, 1953, 1234, 1253]}, "random_specified": {"generated": "2011-03-28T15:17:00.209115+00:00", "data": [1926, 1385, 2469, 3656, 2428, 3058, 3927, 2122, 1166, 1237]}}}
data_url = "/data/"
data = {}

overall_data = ([i,0] for i in [1..10])

generated = null

getData = ->
    $.getJSON data_url, {}, (response) ->
        data = response
        drawGraphs()


drawGraphs = ->
    $("#spinner").hide()
    graph_boxes =
        overall: $("#overview-graph")
        input: $("#input-graph")
        radio: $("#radio-graph")
        select: $("#select-graph")
        slider: $("#slider-graph")
    $("#graphs").show()

    generated = data.input.random_not_specified.generated

    sum = 0
    for method, results of data
        graph_opts = []
        for random_specified in ["random_specified", "random_not_specified"]
            res = results[random_specified]
            label = random_specified.replace(/_/g," ")

            for i in [1..10]
                overall_data[i-1][1] += res.data[i-1]
                sum += res.data[i-1]

            graph_data = ([i,res.data[i-1]] for i in [1..10])
    
            graph_opts.push
                label: label
                bars:
                    show: true
                    align: "center"
                    barwidth : 0.1
                data: graph_data

        $.plot(graph_boxes[method], graph_opts)

    overall_opts =
        bars:
            show: true
            align: "center"
        data: overall_data
    $.plot(graph_boxes.overall, [overall_opts])
    
    $("#as-of").html("For now, here's a preliminary breakdown as of <strong>#{generated}</strong><br>Total votes: <strong>#{sum}</strong>")

init = ->
    getData()

$(document).ready(init)

