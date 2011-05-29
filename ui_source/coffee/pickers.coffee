class Picker
    ###
    Base class for all Pickers.
    ###

    type: ''

    template: ''

    constructor: (@el) ->

    render: ->
        @el.html """
            <div class="method" id="method-#{ @type }">
                #{ @template }
            </div>
            """
    
    setNumber: (new_number) ->
        @number = new_number
        $(this).trigger('picked')


class Input extends Picker
    ###
    Text box that only allows numbers from 1 to 10 to be entered
    (and 0, due to bug).
    ###

    type: 'input'

    template: '<input type="text">'

    render: ->
        super()
        field = @el.find('input')
        field.keypress (e) =>
            if 49 <= e.which <= 57 and field.val() is ''
                @setNumber(e.which - 48)
            else if @number is 1 and e.which is 48
                @setNumber(10)
            else
                e.preventDefault()
        field.focus()



class Radio extends Picker
    ###
    ###

    type: 'radio'

    template: ("<span>#{i}</span>" for i in [1..10]).join('')

    render: ->
        super()
        console.log @el.find('span')
        @el.find('span').click (e) =>
            @setNumber(parseInt $(e.currentTarget).text())



class Select extends Picker
    ###
    ###

    type: 'select'

    template: """
        <span id="selected-num">-</span>
        <ul style="display:none;">
            #{ ("<li>#{i}</li>" for i in [1..10]).join('') }
        </ul>
        """
    
    render: ->
        super()
        list = $("#method-select ul")
        span = $("#method-select span")

        span.mouseover -> list.show()

        $('#method-select li').click (e) =>
            list.hide()
            val = $(e.currentTarget).text()
            span.text(val)
            @setNumber(parseInt val)



class Slider extends Picker
    ###
    ###

    type: 'slider'

    template: '''
        <div id="choice-slider"></div>
        '''
    
    render: ->
        super()
        update = (num) =>
            slider_handle.text(num)
            @setNumber(num)
        $("#choice-slider").slider
            value: 1
            min: 1
            max: 10
            step: 1
            slide: (event, ui) => update(ui.value)
        slider_handle = $("#choice-slider .ui-slider-handle")
        update(1)



#
# Exports
#

window.pickers =
    Input   : Input
    Radio   : Radio
    Select  : Select
    Slider  : Slider
