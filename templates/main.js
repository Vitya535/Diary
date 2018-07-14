$(document).ready(function()
{var line_values,line_clicked;$('th.mon').attr('title','Понедельник');$('th.tue').attr('title','Вторник');$('th.wed').attr('title','Среда');$('th.thu').attr('title','Четверг');$('th.fri').attr('title','Пятница');$('th.sat').attr('title','Суббота');$('th.sun').attr('title','Воскресенье');$('table.month > tbody > tr > td').click(function()
{if($(this).html()!='&nbsp;')
$(this).addClass('active').parents('table.month').children('tbody').find('> tr > td.active').not(this).removeClass('active');});$('div.for_event_lines').mousedown(function(e)
{line_clicked=$(e.target);line_values=$(e.target).html().split('<br>');if(e.button==2)
{$('#delete').offset({top:e.pageY,left:e.pageX});$('#delete').fadeIn();}});$('#delete').click(function()
{$('#description').attr("value",line_values[0]);$('#event_time').attr("value",line_values[1]);var msg=$('#pop_up_form').serialize();$.ajax
({method:'POST',url:'/del_data/',data:msg});$(line_clicked).remove();$(this).fadeOut();});$('body').mousedown(function(e)
{if(e.button!=2||e.target.className!='for_event_lines')
$('#delete').fadeOut();});$('body').contextmenu(function()
{return false;});});$(document).ready(function()
{var line_values,line_clicked;var rows=$('table.month').find('td');$("#what_show :contains('{{cls.buf_for_select}}')").attr('selected','selected');$.each(rows,function(index,value)
{if({{calendar.week_Month}}=={{calendar.Month}})
if({{calendar.week_Year}}=={{calendar.Year}})
if(rows.eq(index).text()=={{calendar.Day}})
rows.eq(index).css('background','#78a2b7');if({{calendar.TODAY_MONTH}}=={{calendar.Month}})
if({{calendar.TODAY_YEAR}}=={{calendar.Year}})
if(rows.eq(index).text()=={{calendar.TODAY_DAY}})
rows.eq(index).css('background','green');});$('#what_show').change(function()
{$('table.show').empty();if($('#what_show option:selected').text()=='День')
{$('#arrow_left').attr('title','Предыдущий день');$('#arrow_right').attr('title','Следующий день');$('#arrow_left').attr('formaction','{{url_for('down_day')}}');$('#arrow_right').attr('formaction','{{url_for('up_day')}}');$('table.show').append('<thead><tr class="scrolling_table"><th id="empty"></th><th class="header scrolling">\
            {{calendar.Day_format}}<br>{{calendar.Day}}</th></thead><tbody class="scrolling_table">');var reg_exp=/[\W]/g
var arr={{calendar.event_data|tojson}};for(var i=0;i<24;i++)
{$('tbody.scrolling_table').append('<tr class="scrolling_table"><td class="empty">'+i+':00-'+(i+1)+':00</td><td class="scrolling"></td></tr>');var td_scroll=$('tbody.scrolling_table').find('td.scrolling')[i];for(var j=0;j<arr.length;j++)
{var split=arr[j][1].split(reg_exp);if(split[0]=={{calendar.Year}})
if(split[1]=={{calendar.Month}})
if(split[2]=={{calendar.Day}})
if(split[3]==i)
$(td_scroll).append('<div class="for_event_lines">'+arr[j][0]+'<br>'+i+':00-'+(i+1)+':00'+'</div>');}}}
else if($('#what_show option:selected').text()=='Неделя')
{$('#arrow_left').attr('title','Предыдущая неделя');$('#arrow_right').attr('title','Следующая неделя');$('#arrow_left').attr('formaction','{{url_for('down_week_vertical')}}');$('#arrow_right').attr('formaction','{{url_for('up_week_vertical')}}');var abridged_day_names=['Пн','Вт','Ср','Чт','Пт','Сб','Вс'];$('table.show').append('<thead><tr class="scrolling_table"><th id="empty"></th>');for(var i=11;i<18;i++)
$('tr.scrolling_table').append('<th class="header">'+abridged_day_names[i-11]+'<br>'+i+'</th>');$('table.show').append('</tr></thead><tbody class="scrolling_table">');for(var i=0;i<24;i++)
{$('tbody.scrolling_table').append('<tr class="scrolling_table"><td class="empty">'+i+':00-'+(i+1)+':00</td>');var tr=$('tbody.scrolling_table').find('tr.scrolling_table')[i];for(var j=0;j<7;j++)
$(tr).append('<td></td>');$('tbody.scrolling_table').append('</tr>');}}
else
{$('#arrow_left').attr('title','Предыдущий месяц');$('#arrow_right').attr('title','Следующий месяц');$('#arrow_left').attr('formaction','{{url_for('down_month')}}');$('#arrow_right').attr('formaction','{{url_for('up_month')}}');var abridged_day_names=['Пн','Вт','Ср','Чт','Пт','Сб','Вс'];$('table.show').append('<thead class="my_id"><tr>');var tr=$('thead.my_id').find('tr');for(var i=0;i<7;i++)
if(28+i>31&&i!=4)
$(tr).append('<th class="header">'+abridged_day_names[i]+'<br>'+(i-3)+'</th>');else if(i==4)
$(tr).append('<th class="header">'+abridged_day_names[i]+'<br>'+(i-3)+' июн'+'</th>');else
$(tr).append('<th class="header">'+abridged_day_names[i]+'<br>'+(28+i)+'</th>');$('thead').append('</tr>');$('table.show').append('</thead><tbody class="my_id">');for(var i=0;i<4;i++)
{$('tbody.my_id').append('<tr>');var tr=$('tbody.my_id').find('tr')[i];for(var j=4;j<11;j++)
if(j==10&&i==3)
$(tr).append('<td class="header">1 июл</td>');else
$(tr).append('<td class="header">'+(j+7*i)+'</td>');$('tbody.my_id').append('</tr>');}}
$('table.show').append('</tbody>');});$('table.show').click(function(e)
{if(e.target.className!='for_event_lines')
{$('button.save').attr('formaction','{{url_for('add_record')}}');var cell_clicked=e.target;if(e.target.id!='empty')
{$('#event_time').attr("value",'{{utils.for_input_time_today(calendar.Day, calendar.Month, calendar.Year)}}'+', '+$(cell_clicked).parent().find('td.empty').text());if(e.target.className=='header scrolling')
$('#event_time').attr("value",'{{utils.for_input_time_today(calendar.Day, calendar.Month, calendar.Year)}}');$('.js_overlay').fadeIn();}
$('.js_overlay').click(function(ev)
{var popup=$('.js_pop_up');if(ev.target!=popup[0]&&popup.has(ev.target).length===0)
$('.js_overlay').fadeOut();});$('.js_close_pop_up').click(function()
{$('.js_overlay').fadeOut();});$('button.save').click(function()
{$('.js_overlay').fadeOut();$(cell_clicked).append('<div class="for_event_lines">'+$('#description').val()+'<br>'+$(cell_clicked).parent().find('td.empty').text()+'</div>');});cell_clicked=null;}});$('div.for_event_lines').click(function(e)
{$('button.save').attr('formaction','{{url_for('update_record')}}');var cell_clicked=e.target;line_values=$(e.target).html().split('<br>');$('#description').attr("value",line_values[0]);$('#event_time').attr("value",line_values[1]);$('#additional_data').attr("value",$(e.target).html());$('.js_overlay').fadeIn();$('.js_overlay').click(function(ev)
{var popup=$('.js_pop_up');if(ev.target!=popup[0]&&popup.has(ev.target).length===0)
$('.js_overlay').fadeOut();});$('.js_close_pop_up').click(function()
{$('.js_overlay').fadeOut();});$('button.save').click(function()
{$('.js_overlay').fadeOut();$(cell_clicked).append('<div class="for_event_lines">'+$('#description').val()+'<br>'+$(cell_clicked).parent().find('td.empty').text()+'</div>');});cell_clicked=null;});});