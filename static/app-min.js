(function(){var j,e,g,f,h,k,d,l,m,i,o,p;h=void 0;e=void 0;g=void 0;f=void 0;k=void 0;i=void 0;if(Math.floor(Math.random()*2)===0){h=true;$("h1 > span").text("Pick a random number from 1 to 10")}else h=false;$("h1").css("color","");d=function(a){o();if(a!=null&&1<=a&&a<=10){$("button").attr("disabled",false);return g=a}else return $("button").attr("disabled","")};l=function(){$("h1").hide();$("#methods").hide();$("button").hide();$("#results-link").hide();return $("#done").show()};m=function(){$("#done").text("There was a problem. Please refresh the page and try again.");
return l()};$("button").click(function(){p();f||(f=0);return $.ajax({url:"/",data:{number:g,method:e,random:h,pick:f,submit:k},type:"POST",dataType:"json",success:function(a){return a.status==="success"?l():m()},error:function(){return m()}})});j=function(a,b){return $(a).each(function(){var c;c=$(this);return $(this).click(function(){$(".selected").removeClass("selected");c.addClass("selected");return typeof b=="function"?b(c):void 0})})};o=function(){return f=new Date-i};p=function(){return k=new Date-
i};[function(){var a;e="input";a=$("#method-input input");a.keypress(function(b){var c;return 49<=(c=b.which)&&c<=57&&a.val()===""?d(b.which-48):g===1&&b.which===48?d(10):false});$("#method-input").show();return a.focus()},function(){var a,b;e="radio";a="";for(b=1;b<=10;b++)a+="<span id='radio-"+b+"'>"+b+"</span>";$("#method-radio").append(a);j("#method-radio span",function(c){return d(parseInt(c.text()))});return $("#method-radio").show()},function(){var a,b,c,n;e="select";a="";for(b=1;b<=10;b++)a+=
"<li id='select-"+b+"'>"+b+"</li>";c=$("#method-select ul");n=$("#method-select span");c.append(a);n.mouseover(function(){return c.show()});j("#method-select li",function(q){c.hide();n.text(q.text());return d(parseInt(q.text()))});return $("#method-select").show()},function(){var a;e="slider";$("#choice-slider").slider({value:1,min:1,max:10,step:1,slide:function(b,c){a.text(c.value);return d(c.value)}});a=$("#choice-slider .ui-slider-handle");a.text(1);d(1);return $("#method-slider").show()}][Math.floor(Math.random()*
4)]();i=new Date}).call(this);