(function() {
  var bindClickToSelect, buildInput, buildRadio, buildSelect, buildSlider, builds, current_method, current_number, current_pick, current_random, current_submit, end, method, sendVote, setNum, showDone, showError, start, startTimer, stopPick, stopSubmit;
  current_random = void 0;
  current_method = void 0;
  current_number = void 0;
  current_pick = void 0;
  current_submit = void 0;
  start = void 0;
  end = void 0;
  if (Math.floor(Math.random() * 2) === 0) {
    current_random = true;
    $("h1 > span").text("Pick a random number from 1 to 10");
  } else {
    current_random = false;
  }
  $("h1").css("color", "");
  setNum = function(num) {
    stopPick();
    if ((num != null) && (1 <= num && num <= 10)) {
      $("button").attr("disabled", false);
      return current_number = num;
    } else {
      return $("button").attr("disabled", "");
    }
  };
  showDone = function() {
    $("h1").hide();
    $("#methods").hide();
    $("button").hide();
    return $("#done").show();
  };
  showError = function() {
    $("#done").text("There was a problem. Please refresh the page and try again.");
    return showDone();
  };
  sendVote = function() {
    var data, error, success;
    stopSubmit();
    success = function(response) {
      if (response.status === "success") {
        return showDone();
      } else {
        return showError();
      }
    };
    error = function() {
      return showError();
    };
    if (!current_pick) {
      current_pick = 0;
    }
    data = {
      number: current_number,
      method: current_method,
      random: current_random,
      pick: current_pick,
      submit: current_submit
    };
    return $.ajax({
      url: "/",
      data: data,
      type: "POST",
      dataType: "json",
      success: success,
      error: error
    });
  };
  $("button").click(sendVote);
  buildInput = function() {
    var field;
    current_method = "input";
    field = $("#method-input input");
    field.keypress(function(e) {
      var _ref;
      if ((49 <= (_ref = e.which) && _ref <= 57) && field.val() === "") {
        return setNum(e.which - 48);
      } else if (current_number === 1 && e.which === 48) {
        return setNum(10);
      } else {
        return false;
      }
    });
    $("#method-input").show();
    return field.focus();
  };
  buildRadio = function() {
    var append_html, extra, i;
    current_method = "radio";
    append_html = "";
    for (i = 1; i <= 10; i++) {
      append_html += "<span id='radio-" + i + "'>" + i + "</span>";
    }
    $("#method-radio").append(append_html);
    extra = function(el) {
      return setNum(parseInt(el.text()));
    };
    bindClickToSelect("#method-radio span", extra);
    return $("#method-radio").show();
  };
  buildSelect = function() {
    var append_html, hOn, i, list, onClick, span;
    current_method = "select";
    append_html = "";
    for (i = 1; i <= 10; i++) {
      append_html += "<li id='select-" + i + "'>" + i + "</li>";
    }
    list = $("#method-select ul");
    span = $("#method-select span");
    list.append(append_html);
    hOn = function() {
      return list.show();
    };
    onClick = function(el) {
      list.hide();
      span.text(el.text());
      return setNum(parseInt(el.text()));
    };
    span.mouseover(hOn);
    bindClickToSelect("#method-select li", onClick);
    return $("#method-select").show();
  };
  buildSlider = function() {
    var slider_handle;
    current_method = "slider";
    $("#choice-slider").slider({
      value: 1,
      min: 1,
      max: 10,
      step: 1,
      slide: function(event, ui) {
        slider_handle.text(ui.value);
        return setNum(ui.value);
      }
    });
    slider_handle = $("#choice-slider .ui-slider-handle");
    slider_handle.text(1);
    setNum(1);
    return $("#method-slider").show();
  };
  bindClickToSelect = function(selector, extra) {
    return $(selector).each(function() {
      var s;
      s = $(this);
      return $(this).click(function() {
        $(".selected").removeClass("selected");
        s.addClass("selected");
        return typeof extra == "function" ? extra(s) : void 0;
      });
    });
  };
  startTimer = function() {
    return start = new Date();
  };
  stopPick = function() {
    return current_pick = new Date() - start;
  };
  stopSubmit = function() {
    return current_submit = new Date() - start;
  };
  builds = [buildInput, buildRadio, buildSelect, buildSlider];
  method = Math.floor(Math.random() * 4);
  builds[method]();
  startTimer();
}).call(this);
