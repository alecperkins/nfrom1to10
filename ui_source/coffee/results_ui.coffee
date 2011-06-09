window.console ?=
  log:->

generated = null

drawGraphs = ->
    main_data = data.ui_breakdown

    $("#spinner").hide()
    $("#graphs").show()
    graph_boxes =
        input       : $("#input-graph")
        radio       : $("#radio-graph")
        select      : $("#select-graph")
        slider      : $("#slider-graph")

    generated = main_data.input.random_not_specified.generated

    sum = 0
    for method, results of main_data
        graph_opts = []
        for random_specified in ["random_specified", "random_not_specified"]
            res = results[random_specified]
            label = random_specified.replace(/_/g," ")
            graph_data = ([i,res.data[i-1]] for i in [1..10])

            graph_opts.push
                label: label
                bars:
                    show: true
                    align: "center"
                    barwidth : 0.1
                data: graph_data
            
        $.plot(graph_boxes[method], graph_opts)


init = ->
    for name, method of window.pickers
        (new method($("##{ name.toLowerCase() }-method"))).render()
    $('.method').show()
    drawGraphs()
    
$(document).ready(init)