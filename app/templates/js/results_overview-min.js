(function(){var l,j,m;if(window.console==null)window.console={log:function(){}};m=function(){var c;c=[];for(j=1;j<=10;j++)c.push([j,0]);return c}();l=null;$(document).ready(function(){var c,h,e,d,b,k,a,n,f,i,o,g,r,p;c=data.ui_breakdown;e=data.over_time;k={overall:$("#overview-graph"),overtime:$("#overtime-graph"),country:$("#country-graph")};l=c.input.random_not_specified.generated;o=0;for(f in c){b=c[f];p=["random_specified","random_not_specified"];g=0;for(r=p.length;g<r;g++){i=p[g];i=b[i];for(a=
1;a<=10;a++){m[a-1][1]+=i.data[a-1];o+=i.data[a-1]}}}$.plot(k.overall,[{bars:{show:true,align:"center"},data:m}]);c=[];b=[];g=f=0;for(d in e){b=e[d];if(b.length>0){f=b[0][0];g=b[b.length-1][0];c.push({label:(parseInt(d)+1).toString(),lines:{show:true},data:b})}}e=(g-f)/4;b=[f];for(a=1;a<=4;a++){d=f+e*a;b.push(d)}a=0;for(e=b.length;0<=e?a<e:a>e;0<=e?a++:a--){d=new Date(b[a]*1E3);b[a]=[b[a],""+d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate()+" "+d.getHours()+":"+d.getMinutes()]}$.plot(k.overtime,
c,{xaxis:{ticks:b}});e=[];for(h in country_data){c=country_data[h];d=[];b=c.data;for(n in b){f=b[n];d.push([parseInt(n),f/c.total])}e.push({label:h,lines:{show:true},data:d})}h={xaxis:{ticks:function(){var q;q=[];for(a=1;a<=10;a++)q.push([a,a]);return q}()}};$.plot(k.country,e,h);return $("#as-of").html("Here's an overview as of <strong>"+l+"</strong><br>Total votes: <strong>"+o+"</strong>")})}).call(this);