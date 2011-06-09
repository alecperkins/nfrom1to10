(function() {
  var Quiz, follow_ups;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  follow_ups = {
    how: {
      '1': 'Thought of a number and chose it',
      '2': 'Used a die, random number generator, or other random process',
      '3': 'Looked around me for a number',
      '4-input': 'Mashed the keyboard',
      '4-radio': 'Moved the mouse back-and-forth quickly then clicked',
      '4-select': 'Moved the mouse back-and-forth quickly then clicked',
      '4-slider': 'Moved the slider back-and-forth quickly then released',
      '5': 'Other'
    },
    why: {
      '1': 'Yes, it is personally significant',
      '2': 'Yes, it is culturally significant',
      '3': 'No, it is arbitrary'
    }
  };
  Quiz = (function() {
    /*
        Class for managing the quiz flow. The whole thing is procedural, really.
        This is just used to namespace everything.
        */    var t_start;
    t_start = null;
    function Quiz() {
      this.submitFollowup = __bind(this.submitFollowup, this);
      this.submit = __bind(this.submit, this);      var choice;
      if (Math.floor(Math.random() * 2) === 0) {
        this.current_random = true;
        $("h1 > span").text("Pick a random number from 1 to 10");
      } else {
        this.current_random = false;
      }
      $("h1").css("color", "");
      this.number = null;
      choice = window.picker_options[Math.floor(Math.random() * 4)];
      this.active_picker = new window.pickers[choice]($('#methods'));
      this.active_picker.render();
      this.els = {
        submit_number: $('#submit-number'),
        submit_followup: $('#submit-followup'),
        method_container: $('#methods'),
        methods: $('.method'),
        followup: $('#follow-up'),
        done: $('#done')
      };
      $(this.active_picker).bind('picked', __bind(function() {
        var _ref;
                if ((_ref = this.t_pick) != null) {
          _ref;
        } else {
          this.t_pick = new Date() - t_start;
        };
        return this.els.submit_number.attr('disabled', false);
      }, this));
      if (this.active_picker.type === 'slider') {
        $(this.active_picker).trigger('picked');
      }
      this.els.submit_number.click(this.submit);
      this.els.submit_followup.click(this.submitFollowup);
      this.els.methods.show();
      this.els.method_container.show();
      t_start = new Date();
    }
    Quiz.prototype.submit = function() {
      var data, _ref;
      console.log(this.active_picker.number);
            if ((_ref = this.t_submit) != null) {
        _ref;
      } else {
        this.t_submit = new Date() - t_start;
      };
      data = {
        number: this.active_picker.number,
        method: this.active_picker.type,
        random: this.current_random,
        pick: this.t_pick,
        submit: this.t_submit,
        range: this.active_picker.range
      };
      console.log(data);
      return $.post('/vote/', data, __bind(function(response) {
        console.log(response);
        if (response.status === 'success') {
          this.vote_id = response.vote_id;
          return this.showFollowup();
        }
      }, this), "json");
    };
    Quiz.prototype.showFollowup = function() {
      var i, renderItem, x, _fn, _fn2;
      this.els.methods.hide();
      $('span.num').text(this.active_picker.number);
      renderItem = function(category, item, extra) {
        var label;
        if (extra == null) {
          extra = '';
        }
        label = follow_ups[category][item];
        return $("<li>" + label + extra + "</li>");
      };
      _fn = __bind(function() {
        var x, x_id;
        x_id = i;
        x = renderItem('how', "" + i);
        x.click(__bind(function() {
          this.followup_how = x_id;
          $('input[type="text"]').css('opacity', '0.3');
          $('#how .selected').removeClass('selected');
          x.addClass('selected');
          return this.enableSubmitFollowup();
        }, this));
        return $('#how').append(x);
      }, this);
      for (i = 1; i <= 4; i++) {
        if (i === 4) {
          i = "" + i + "-" + this.active_picker.type;
        }
        _fn();
      }
      x = renderItem('how', 5, '<input id="follow-up-how-other" type="text" style="opacity:0.3" placeholder="Please describe the method you used.">');
      x.click(__bind(function() {
        $('#follow-up-how-other').keydown(__bind(function() {
          return this.followup_how = $('#follow-up-how-other').val();
        }, this));
        $('input[type="text"]').css('opacity', '1');
        $('#how .selected').removeClass('selected');
        x.addClass('selected');
        console.log(this.followup_how);
        return this.enableSubmitFollowup();
      }, this));
      $('#how').append(x);
      _fn2 = __bind(function() {
        var y, y_id;
        y_id = i;
        y = renderItem('why', "" + i);
        y.click(__bind(function() {
          this.followup_why = y_id;
          $('#why .selected').removeClass('selected');
          y.addClass('selected');
          return this.enableSubmitFollowup();
        }, this));
        return $('#why').append(y);
      }, this);
      for (i = 1; i <= 3; i++) {
        _fn2();
      }
      return this.els.followup.show();
    };
    Quiz.prototype.submitFollowup = function() {
      var data;
      data = {
        vote_id: this.vote_id,
        how: "" + this.followup_how,
        why: "" + this.followup_why
      };
      console.log(data);
      return $.post('/followup/', data, __bind(function(response) {
        console.log(response);
        if (response.status === 'success') {
          return this.showDone();
        }
      }, this), "json");
    };
    Quiz.prototype.enableSubmitFollowup = function() {
      if ((this.followup_why != null) && (this.followup_how != null)) {
        return this.els.submit_followup.attr('disabled', false);
      }
    };
    Quiz.prototype.showDone = function() {
      this.els.followup.hide();
      return this.els.done.show();
    };
    return Quiz;
  })();
  $(document).ready(function() {
    return new Quiz();
  });
}).call(this);
