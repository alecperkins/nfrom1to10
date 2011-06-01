follow_ups =
    how:
        '1'         : 'Thought of a number and chose it'
        '2'         : 'Used a die, random number generator, or other random process'
        '3'         : 'Looked around me for a number'
        '4-input'   : 'Mashed the keyboard'
        '4-radio'   : 'Moved the mouse back-and-forth quickly then clicked'
        '4-select'  : 'Moved the mouse back-and-forth quickly then clicked'
        '4-slider'  : 'Moved the slider back-and-forth quickly then released'
        '5'         : 'Other'
    why:
        '1'         : 'Yes, it is personally significant'
        '2'         : 'Yes, it is culturally significant'
        '3'         : 'No, it is arbitrary'

class Quiz
    ###
    Class for managing the quiz flow. The whole thing is procedural, really.
    This is just used to namespace everything.
    ###

    t_start = null

    constructor: ->
        if Math.floor(Math.random()*2) is 0
            current_random = true
            $("h1 > span").text("Pick a random number from 1 to 10")
        else
            current_random = false
        $("h1").css("color","")

        @number = null
        choice = window.picker_options[Math.floor(Math.random()*4)]
        @active_picker = new window.pickers[choice]($('#methods'))
        @active_picker.render()
        @els =
            submit_number       : $('#submit-number')
            submit_followup     : $('#submit-followup')
            method_container    : $('#methods')
            methods             : $('.method')
            followup            : $('#follow-up')
            done                : $('#done')
        $(@active_picker).bind 'picked', =>
            @t_pick ?= (new Date() - t_start)
            @els.submit_number.attr('disabled',false)

        if @active_picker.type is 'slider'
            $(@active_picker).trigger('picked')

        @els.submit_number.click @submit
        @els.submit_followup.click @submitFollowup
        @els.methods.show()
        @els.method_container.show()
        t_start = new Date()

    submit: =>
        console.log @active_picker.number
        @t_submit ?= (new Date() - t_start)
        data =
            number  : @active_picker.number
            method  : @active_picker.type
            random  : true
            pick    : @t_pick
            submit  : @t_submit
            range   : @active_picker.range
        console.log data
        $.post '/vote/', data, (response) =>
            console.log response
            if response.status is 'success'
                @vote_id = response.vote_id
                @showFollowup()
        , "json"

    showFollowup: ->
        @els.methods.hide()

        $('span.num').text @active_picker.number
        renderItem = (category, item, extra='') ->
            label = follow_ups[category][item]
            return $("""<li>#{ label }#{ extra }</li>""")

        for i in [1..4]
            if i is 4
                i = "#{ i }-#{ @active_picker.type }"
            (=>
                x_id = i
                x = renderItem('how', "#{ i }")
                x.click =>
                    @followup_how = x_id
                    $('input[type="text"]').css('opacity','0.3')
                    $('#how .selected').removeClass('selected')
                    x.addClass('selected')
                    @enableSubmitFollowup()
                $('#how').append(x)
            )()
        
        x = renderItem('how', 5, '<input id="follow-up-how-other" type="text" style="opacity:0.3" placeholder="Please describe the method you used.">')
        x.click =>
            $('#follow-up-how-other').keydown =>
                @followup_how = $('#follow-up-how-other').val()
            $('input[type="text"]').css('opacity','1')
            $('#how .selected').removeClass('selected')
            x.addClass('selected')
            console.log @followup_how
            @enableSubmitFollowup()
        $('#how').append(x)
        
        for i in [1..3]
            (=>
                y_id = i
                y = renderItem('why', "#{ i }")
                y.click =>
                    @followup_why = y_id
                    $('#why .selected').removeClass('selected')
                    y.addClass('selected')
                    @enableSubmitFollowup()
                $('#why').append(y)
            )()
        
        @els.followup.show()

    submitFollowup: =>
        data =
            vote_id : @vote_id
            how     : "#{ @followup_how }"
            why     : "#{ @followup_why }"
        console.log data
        $.post '/followup/', data, (response) =>
            console.log response
            if response.status is 'success'
                @showDone()
        , "json"

    enableSubmitFollowup: ->
        if @followup_why? and @followup_how?
            @els.submit_followup.attr('disabled',false)
    
    showDone: ->
        @els.followup.hide()
        @els.done.show()

$(document).ready -> new Quiz()