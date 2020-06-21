$(document).ready(function()
{
    // line_clicked - событие, которое было кликнуто
    // line_values - значения названия события и время события
    let line_values;
    let $tableShow = $('table.show');
    let $arrowLeft = $('#arrow_left');
    let $arrowRight = $('#arrow_right');
    let $whatShow = $('#what_show option:selected');
    let $scrollingTable = $('tbody.scrolling_table');
    let $tbodyMyId = $('tbody.my_id');
    let $buttonSave = $('button.save');
    let $eventTime = $('#event_time');
    let $jsOverlay = $('.js_overlay');
    const rows = $('table.month').find('td');
    $("#what_show :contains('{{cls.buf_for_select}}')").attr('selected', 'selected');
    $.each(rows, function(index)
    {
        // подсветка дня на котором находимся
        if ({{calendar.week_month}} === {{calendar.month}})
            if ({{calendar.week_year}} === {{calendar.year}})
                if (rows.eq(index).text() === {{calendar.day}})
                    rows.eq(index).css('background', '#78a2b7');

        // подсветка сегодняшнего дня
        if ({{calendar.today_month}} === {{calendar.month}})
            if ({{calendar.today_year}} === {{calendar.year}})
                if ({{calendar.today_day}} === rows.eq(index).text())
                    rows.eq(index).css('background', 'green');
    });

    // функция в зависимости от контекста, отображающая календарь в виде таблицы-ежедневника на определенный период
    $('#what_show').on('change',function()
    {
        let tr, abridged_day_names, j, i;
        $tableShow.empty();
        if ($whatShow.text() === 'День')
        {
            $arrowLeft.attr('title', 'Предыдущий день');
            $arrowRight.attr('title', 'Следующий день');
            $arrowLeft.attr('formaction', '{{url_for('down_day')}}');
            $arrowRight.attr('formaction', '{{url_for('up_day')}}');
            $('table.show').append('<thead><tr class="scrolling_table"><th id="empty"></th><th class="header scrolling">\
            {{calendar.day_format}}<br>{{calendar.day}}</th></thead><tbody class="scrolling_table">');
            let reg_exp = /[\W]/g;
            let arr = {{calendar.event_data|tojson}};
            for (i = 0; i < 24; i++)
            {
                $scrollingTable.append('<tr class="scrolling_table"><td class="empty">' + i + ':00-' + (i + 1) + ':00</td><td class="scrolling"></td></tr>');
                let td_scroll = $scrollingTable.find('td.scrolling')[i];
                for (j = 0; j < arr.length; j++)
                {
                    let split = arr[j][1].split(reg_exp);
                    if (split[0] === {{calendar.year}})
                        if (split[1] === {{calendar.month}})
                            if (split[2] === {{calendar.day}})
                                if (split[3] === i)
                                    $(td_scroll).append('<div class="for_event_lines">' + arr[j][0] + '<br>' + i + ':00-' + (i + 1) + ':00' + '</div>');
                }
            }
        }
        else if ($whatShow.text() === 'Неделя')
        {
            $arrowLeft.attr('title', 'Предыдущая неделя');
            $arrowRight.attr('title', 'Следующая неделя');
            $arrowLeft.attr('formaction', '{{url_for('down_week_vertical')}}');
            $arrowRight.attr('formaction', '{{url_for('up_week_vertical')}}');
            abridged_day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
            $tableShow.append('<thead><tr class="scrolling_table"><th id="empty"></th>');
            for (i = 11; i < 18; i++)
                $('tr.scrolling_table').append('<th class="header">' + abridged_day_names[i - 11] + '<br>' + i + '</th>');
            $tableShow.append('</tr></thead><tbody class="scrolling_table">');
            for (i = 0; i < 24; i++)
            {
                $scrollingTable.append('<tr class="scrolling_table"><td class="empty">' + i + ':00-' + (i + 1) + ':00</td>');
                tr = $scrollingTable.find('tr.scrolling_table')[i];
                for (j = 0; j < 7; j++)
                    $(tr).append('<td></td>');
                $scrollingTable.append('</tr>');
            }
        }
        else
        {
            $arrowLeft.attr('title', 'Предыдущий месяц');
            $arrowRight.attr('title', 'Следующий месяц');
            $arrowLeft.attr('formaction', '{{url_for('down_month')}}');
            $arrowRight.attr('formaction', '{{url_for('up_month')}}');
            abridged_day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
            $tableShow.append('<thead class="my_id"><tr>');
            tr = $('thead.my_id').find('tr');
            for (i = 0; i < 7; i++)
                if (28 + i > 31 && i !== 4)
                    $(tr).append('<th class="header">' + abridged_day_names[i] + '<br>' + (i - 3) + '</th>');
                else if (i === 4)
                    $(tr).append('<th class="header">' + abridged_day_names[i] + '<br>' + (i - 3) + ' июн' + '</th>');
                else
                    $(tr).append('<th class="header">' + abridged_day_names[i] + '<br>' + (28 + i) + '</th>');
            $('thead').append('</tr>');
            $tableShow.append('</thead><tbody class="my_id">');
            for (i = 0; i < 4; i++)
            {
                $tbodyMyId.append('<tr>');
                tr = $tbodyMyId.find('tr')[i];
                for (j = 4; j < 11; j++)
                    if (j === 10 && i === 3)
                        $(tr).append('<td class="header">1 июл</td>');
                    else
                        $(tr).append('<td class="header">' + (j + 7*i) + '</td>');
                $tbodyMyId.append('</tr>');
            }
        }
        $tableShow.append('</tbody>');
    });

    // здесь добавление события
    $tableShow.on('click', function(e)
    {
        // если кликнули не на событие
        if (e.target.className !== 'for_event_lines')
        {
            $buttonSave.attr('formaction', '{{url_for('add_record')}}');
            let cell_clicked = e.target;
            if (e.target.id !== 'empty')
            {
                // открытие всплывающей формы по клику на ячейку
                $eventTime.attr("value", '{{utils.for_input_time_today(calendar.day, calendar.month, calendar.year)}}' + ', ' + $(cell_clicked).parent().find('td.empty').text());
                if (e.target.className === 'header scrolling')
                    $eventTime.attr("value", '{{utils.for_input_time_today(calendar.day, calendar.month, calendar.year)}}');
                $jsOverlay.fadeIn();
            }

            // закрытие всплывающей формы по клику вне окна
            $jsOverlay.on('click', function(ev)
            {
                let popup = $('.js_pop_up');
                if (ev.target !== popup[0] && popup.has(ev.target).length === 0)
                    $jsOverlay.fadeOut();
            });

            // закрытие всплывающей формы по клику на крестик
            $('.js_close_pop_up').on('click', function()
            {
                $jsOverlay.fadeOut();
            });

            // закрытие всплывающей формы по клику на кнопку "Сохранить" и добавление события
            $buttonSave.on('click', function()
            {
                $jsOverlay.fadeOut();
                $(cell_clicked).append('<div class="for_event_lines">' + $('#description').val() + '<br>' + $(cell_clicked).parent().find('td.empty').text() + '</div>');
            });
            cell_clicked = null;
        }
    });

    // редактирование события
    $('div.for_event_lines').on('click', function(e)
    {
        $buttonSave.attr('formaction', '{{url_for('update_record')}}');
        let cell_clicked = e.target;
        line_values = $(e.target).html().split('<br>');
        $('#description').attr("value", line_values[0]);
        $eventTime.attr("value", line_values[1]);
        $('#additional_data').attr("value", $(e.target).html());
        $jsOverlay.fadeIn();

        // закрытие всплывающей формы по клику вне окна
        $jsOverlay.on('click', function(ev)
        {
            let popup = $('.js_pop_up');
            if (ev.target !== popup[0] && popup.has(ev.target).length === 0)
                $jsOverlay.fadeOut();
        });

        // закрытие всплывающей формы по клику на крестик
        $('.js_close_pop_up').on('click', function()
        {
            $jsOverlay.fadeOut();
        });

        // закрытие всплывающей формы по клику на кнопку "Сохранить" и редактирование события
        $('button.save').on('click', function()
        {
            $jsOverlay.fadeOut();
            $(cell_clicked).append('<div class="for_event_lines">' + $('#description').val() + '<br>' + $(cell_clicked).parent().find('td.empty').text() + '</div>');
        });
        cell_clicked = null;
    });
});