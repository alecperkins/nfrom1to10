current_random = undefined
current_method = undefined
current_number = undefined
current_pick = undefined
current_submit = undefined

start = undefined
end = undefined

if Math.floor(Math.random()*2) is 0
    current_random = true
    $("h1 > span").text("Pick a random number from 1 to 10")
else
    current_random = false
$("h1").css("color","")







setNum = (num) ->
    stopPick()
    if num? and 1 <= num <= 10
        $("button").attr("disabled",false)
        current_number = num
    else
        $("button").attr("disabled","")

showDone = ->
    $("h1").hide()
    $("#methods").hide()
    $("button").hide()
    $("#done").show()

showError = ->
    $("#done").text("There was a problem. Please refresh the page and try again.")
    showDone()

sendVote = ->
    stopSubmit()
    success = (response) ->
        if response.status is "success"
            showDone()
        else
            showError()
    error = ->
        showError()
    data =
        number: current_number
        method: current_method
        random: current_random
        pick: current_pick
        submit: current_submit
    $.ajax
        url: "/"
        data: data
        type: "POST"
        dataType: "json"
        success: success
        error: error

$("button").click sendVote

buildInput = ->
    current_method = "input"
    field = $("#method-input input")
    field.keypress (e) ->
        if 49 <= e.which <= 57 and field.val() is ""
            setNum(e.which - 48)
        else if current_number is 1 and e.which is 48
            setNum(10)
        else
            return false
    $("#method-input").show()
    field.focus()

buildRadio = ->
    current_method = "radio"
    append_html = ""
    append_html += "<span id='radio-#{i}'>#{i}</span>" for i in [1..10]
    $("#method-radio").append(append_html)
    extra = (el) ->
        setNum(parseInt(el.text()))
    bindClickToSelect("#method-radio span", extra)
    $("#method-radio").show()

buildSelect = ->
    current_method = "select"
    append_html = ""
    append_html += "<li id='select-#{i}'>#{i}</li>" for i in [1..10]
    list = $("#method-select ul")
    span = $("#method-select span")
    list.append(append_html)
    
    hOn = ->
        list.show()
    onClick = (el) ->
        list.hide()
        span.text(el.text())
        setNum(parseInt(el.text()))
    span.mouseover(hOn)
            
    bindClickToSelect("#method-select li", onClick)
    $("#method-select").show()

buildSlider = ->
    current_method = "slider"
    $("#choice-slider").slider
        value: 1
        min: 1
        max: 10
        step: 1
        slide: (event, ui) ->
            slider_handle.text(ui.value)
            setNum(ui.value)
    slider_handle = $("#choice-slider .ui-slider-handle")
    slider_handle.text(1)
    setNum(1)
    $("#method-slider").show()




bindClickToSelect = (selector, extra) ->
    $(selector).each ->
        s = $(this)
        $(this).click ->
            $(".selected").removeClass("selected")
            s.addClass("selected")
            extra?(s)


startTimer = ->
    start = new Date()

stopPick = ->
    current_pick = new Date() - start

stopSubmit = ->
    current_submit = new Date() - start


builds = [buildInput, buildRadio, buildSelect, buildSlider]

method = Math.floor(Math.random()*4)
builds[method]()
startTimer()
