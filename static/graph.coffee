# data = {"input": {"generated": "2011-03-28T03:04:43.279884Z", "data": [2320, 2983, 3981, 4467, 4043, 3897, 6124, 3843, 2617, 1527]}, "radio": {"generated": "2011-03-28T03:04:44.770577", "data": [2343, 2905, 4059, 5491, 3901, 4462, 6037, 3157, 2329, 2199]}, "select": {"generated": "2011-03-28T03:04:47.200486", "data": [2034, 2617, 3784, 4313, 7725, 5606, 6648, 3895, 2297, 2133]}, "slider": {"generated": "2011-03-28T03:04:41.414317", "data": [2290, 2099, 3841, 5634, 3835, 4668, 5869, 3163, 1807, 1896]}}
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

    generated = new Date(data.input.generated)

    sum = 0
    for method, results of data
        for i in [1..10]
            overall_data[i-1][1] += results.data[i-1]
            sum += results.data[i-1]

        graph_data = ([i,results.data[i-1]] for i in [1..10])
        
        graph_opts =
            bars:
                show: true
                align: "center"
            data: graph_data
        $.plot(graph_boxes[method], [graph_opts])

    overall_opts =
        bars:
            show: true
            align: "center"
        data: overall_data
    $.plot(graph_boxes.overall, [overall_opts])
    
    $("#as-of").html("For now, here's a preliminary breakdown as of <strong>#{generated.toGMTString()}</strong><br>Total votes: <strong>#{sum}</strong>")

init = ->
    getData()

$(document).ready(init)

