(function() {
  var Input, Picker, Radio, Select, Slider;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  }, __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  Picker = (function() {
    /*
        Base class for all Pickers. Bind to the Picker instance's `picked` event
        to detect when a number has been picked. The `number` attribute has the
        currently chosen number for that Picker instance. By default, the number
        is undefined.
        */    Picker.prototype.type = '';
    Picker.prototype.template = '';
    function Picker(el) {
      this.el = el;
      this.range = '1-10';
    }
    Picker.prototype.render = function() {
      return this.el.html("<div class=\"method\" id=\"method-" + this.type + "\">\n    " + this.template + "\n</div>");
    };
    Picker.prototype.setNumber = function(new_number) {
      this.number = new_number;
      return $(this).trigger('picked');
    };
    return Picker;
  })();
  Input = (function() {
    __extends(Input, Picker);
    function Input() {
      Input.__super__.constructor.apply(this, arguments);
    }
    /*
        Text box that only allows numbers from 1 to 10 to be entered
        (and 0, due to bug).
        */
    Input.prototype.type = 'input';
    Input.prototype.template = '<input type="text">';
    Input.prototype.render = function() {
      var field;
      Input.__super__.render.call(this);
      field = this.el.find('input');
      field.keypress(__bind(function(e) {
        var _ref;
        if ((49 <= (_ref = e.which) && _ref <= 57) && field.val() === '') {
          return this.setNumber(e.which - 48);
        } else if (this.number === 1 && e.which === 48) {
          return this.setNumber(10);
        } else {
          return e.preventDefault();
        }
      }, this));
      return field.focus();
    };
    return Input;
  })();
  Radio = (function() {
    var i;
    __extends(Radio, Picker);
    function Radio() {
      Radio.__super__.constructor.apply(this, arguments);
    }
    /*
        All the possible numbers, arranged in a list. Numbers are selected like a
        standard radio list, where only one item can be selected at a time.
        */
    Radio.prototype.type = 'radio';
    Radio.prototype.template = ((function() {
      var _results;
      _results = [];
      for (i = 1; i <= 10; i++) {
        _results.push("<span>" + i + "</span>");
      }
      return _results;
    })()).join('');
    Radio.prototype.render = function() {
      Radio.__super__.render.call(this);
      return this.el.find('span').click(__bind(function(e) {
        var $el;
        $el = $(e.currentTarget);
        this.el.find('span.selected').removeClass('selected');
        $el.addClass('selected');
        return this.setNumber(parseInt($el.text()));
      }, this));
    };
    return Radio;
  })();
  Select = (function() {
    var i;
    __extends(Select, Picker);
    function Select() {
      Select.__super__.constructor.apply(this, arguments);
    }
    /*
        All the possible numbers, arranged in a list that is only visible after
        the user hovers over the item. Like a standard <select>, only one item can
        be selected at a time.
        */
    Select.prototype.type = 'select';
    Select.prototype.template = "<span id=\"selected-num\">-</span>\n<ul style=\"display:none;\">\n    " + (((function() {
      var _results;
      _results = [];
      for (i = 1; i <= 10; i++) {
        _results.push("<li>" + i + "</li>");
      }
      return _results;
    })()).join('')) + "\n</ul>";
    Select.prototype.render = function() {
      var list, span;
      Select.__super__.render.call(this);
      list = $("#method-select ul");
      span = $("#method-select span");
      span.mouseover(function() {
        return list.show();
      });
      return $('#method-select li').click(__bind(function(e) {
        var val;
        list.hide();
        val = $(e.currentTarget).text();
        span.text(val);
        return this.setNumber(parseInt(val));
      }, this));
    };
    return Select;
  })();
  Slider = (function() {
    __extends(Slider, Picker);
    function Slider() {
      Slider.__super__.constructor.apply(this, arguments);
    }
    /*
        A slider with start, end, and increments for the range of possible numbers.
        Unlike other Pickers, the Slider has a default value of 1.
        */
    Slider.prototype.type = 'slider';
    Slider.prototype.template = '<div id="choice-slider"></div>';
    Slider.prototype.render = function() {
      var slider_handle, update;
      Slider.__super__.render.call(this);
      update = __bind(function(num) {
        slider_handle.text(num);
        return this.setNumber(num);
      }, this);
      $("#choice-slider").slider({
        value: 1,
        min: 1,
        max: 10,
        step: 1,
        slide: __bind(function(event, ui) {
          return update(ui.value);
        }, this)
      });
      slider_handle = $("#choice-slider .ui-slider-handle");
      return update(1);
    };
    return Slider;
  })();
  window.pickers = {
    Input: Input,
    Radio: Radio,
    Select: Select,
    Slider: Slider
  };
  window.picker_options = ['Input', 'Radio', 'Select', 'Slider'];
}).call(this);
