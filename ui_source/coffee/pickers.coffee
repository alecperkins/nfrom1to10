class Picker
    ###
    Base class for all Pickers. Bind to the Picker instance's `picked` event
    to detect when a number has been picked. The `number` attribute has the
    currently chosen number for that Picker instance. By default, the number
    is undefined.
    ###

    type: ''

    template: ''

    constructor: (@el) ->
        @range = '1-10'

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
    All the possible numbers, arranged in a list. Numbers are selected like a
    standard radio list, where only one item can be selected at a time.
    ###

    type: 'radio'

    template: ("<span>#{i}</span>" for i in [1..10]).join('')

    render: ->
        super()
        @el.find('span').click (e) =>
            $el = $(e.currentTarget)
            @el.find('span.selected').removeClass('selected')
            $el.addClass('selected')
            @setNumber(parseInt $el.text())



class Select extends Picker
    ###
    All the possible numbers, arranged in a list that is only visible after
    the user hovers over the item. Like a standard <select>, only one item can
    be selected at a time.
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
    A slider with start, end, and increments for the range of possible numbers.
    Unlike other Pickers, the Slider has a default value of 1.
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

window.picker_options = [
    'Input'
    'Radio'
    'Select'
    'Slider'
]