// jquery.pjax.js
// copyright chris wanstrath
// https://github.com/defunkt/jquery-pjax
(function(b){b.fn.pjax=function(a,c){c?c.container=a:c=b.isPlainObject(a)?a:{container:a};if(typeof c.container!=="string")throw"pjax container must be a string selector!";return this.live("click",function(a){if(a.which>1||a.metaKey)return!0;var d={url:this.href,container:b(this).attr("data-pjax"),clickedElement:b(this)};b.pjax(b.extend({},d,c));a.preventDefault()})};b.pjax=function(a){var c=b(a.container),g=a.success||b.noop;delete a.success;if(typeof a.container!=="string")throw"pjax container must be a string selector!";
a=b.extend(!0,{},{timeout:650,push:!0,replace:!1,data:{_pjax:!0},type:"GET",dataType:"html",beforeSend:function(a){c.trigger("start.pjax");a.setRequestHeader("X-PJAX","true")},error:function(){window.location=a.url},complete:function(){c.trigger("end.pjax")},success:function(d){if(!b.trim(d)||/<html/i.test(d))return window.location=a.url;c.html(d);var f=document.title,e=b.trim(c.find("title").remove().text());if(e)document.title=e;var e={pjax:a.container,timeout:a.timeout},h=b.param(a.data);if(h!=
"_pjax=true")e.url=a.url+(/\?/.test(a.url)?"&":"?")+h;if(a.replace)window.history.replaceState(e,document.title,a.url);else if(a.push){if(!b.pjax.active)window.history.replaceState(b.extend({},e,{url:null}),f),b.pjax.active=!0;window.history.pushState(e,document.title,a.url)}(a.replace||a.push)&&window._gaq&&_gaq.push(["_trackPageview"]);f=window.location.hash.toString();if(f!=="")window.location.hash="",window.location.hash=f;g.apply(this,arguments)}},a);if(b.isFunction(a.url))a.url=a.url();var d=
b.pjax.xhr;if(d&&d.readyState<4)d.onreadystatechange=b.noop,d.abort();b.pjax.xhr=b.ajax(a);b(document).trigger("pjax",b.pjax.xhr,a);return b.pjax.xhr};var g="state"in window.history,i=location.href;b(window).bind("popstate",function(a){var c=!g&&location.href==i;g=!0;if(!c&&(a=a.state)&&a.pjax)c=a.pjax,b(c+"").length?b.pjax({url:a.url||location.href,container:c,push:!1,timeout:a.timeout}):window.location=location.href});b.inArray("state",b.event.props)<0&&b.event.props.push("state");b.support.pjax=
window.history&&window.history.pushState;if(!b.support.pjax)b.pjax=function(a){window.location=b.isFunction(a.url)?a.url():a.url},b.fn.pjax=function(){return this}})(jQuery);