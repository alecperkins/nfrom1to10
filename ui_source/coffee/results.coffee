window.console ?=
  log:->

data_url = "/data/results"
data = {}




overall_data = ([i,0] for i in [1..10])

generated = null

getData = ->
    $.get data_url, {}, (response) ->
         data = response
         drawGraphs()
    , "json"
    #drawGraphs()



drawGraphs = ->
    main_data = data.breakdown
    time_data = data.overtime

    $("#spinner").hide()
    $("#graphs").show()
    graph_boxes =
        overall     : $("#overview-graph")
        input       : $("#input-graph")
        radio       : $("#radio-graph")
        select      : $("#select-graph")
        slider      : $("#slider-graph")
        overtime    : $("#overtime-graph")
        country     : $("#country-graph")

    generated = main_data.input.random_not_specified.generated

    sum = 0
    for method, results of main_data
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
    
    # graph_data = ([i,res.data[i-1]] for i in [1..10])
    time_opts = []

    ticks = []

    t_start = 0
    t_end = 0
    for num, datas of time_data
        # console.log datas[0]
        t_start = datas[0][0]
        t_end = datas[datas.length-1][0]
        
        time_opts.push
            label: (parseInt(num) + 1).toString()
            lines:
                show: true
            data: datas

    t_diff = (t_end - t_start) / 4
    ticks = [t_start]
    for i in [1..4]
        new_t = t_start + (t_diff * i)
        ticks.push(new_t)
    
    for i in [0...ticks.length]
        d = new Date(ticks[i] * 1000)
        ticks[i] = [ticks[i],"#{d.getFullYear()}-#{d.getMonth()+1}-#{d.getDate()} #{d.getHours()}:#{d.getMinutes()}"]

    time_settings =
        xaxis:
            ticks: ticks

    $.plot(graph_boxes.overtime, time_opts, time_settings)
    
    
    # {US:{data:{"1":8782,"2":9891,"3":15130,"4":19064,"5":14047,"6":17968,"7":24062,"8":13477,"9":8442,"10":6827},total:137690},
    
    
    country_graph_data = []
    for country, cdata of country_data
        d = []
        for k, v of cdata.data
            d.push([parseInt(k),v/cdata.total])
        country_graph_data.push
            label: country
            lines:
                show: true
            data: d
    
    country_graph_settings =
        xaxis:
            ticks: ([i,i] for i in [1..10])

    $.plot(graph_boxes.country, country_graph_data, country_graph_settings)
    
    $("#as-of").html("Here's a breakdown as of <strong>#{generated}</strong><br>Total votes: <strong>#{sum}</strong>")

init = ->
    getData()
    for name, method of window.pickers
        (new method($("##{ name.toLowerCase() }-method"))).render()
    $('.method').show()

$(document).ready(init)
