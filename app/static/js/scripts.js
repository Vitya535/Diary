$(document).ready(function () {
    // line_clicked - событие, которое было кликнуто
    // line_values - значения названия события и время события
    let line_values, line_clicked;
    let $body = $('body');
    // здесь даются всплывающие подсказки для дней недели в календаре
    $('th.mon').attr('title', 'Понедельник');
    $('th.tue').attr('title', 'Вторник');
    $('th.wed').attr('title', 'Среда');
    $('th.thu').attr('title', 'Четверг');
    $('th.fri').attr('title', 'Пятница');
    $('th.sat').attr('title', 'Суббота');
    $('th.sun').attr('title', 'Воскресенье');

    // данная функция добавляет подсветку ячейке календаря по клику на нее
    $('table.month > tbody > tr > td').on('click', function () {
        if ($(this).html() !== '&nbsp;')
            $(this).addClass('active').parents('table.month').children('tbody').find('> tr > td.active').not(this).removeClass('active');
    });

    // в этом блоке - удаление события из таблицы-ежедневника
    // данная функция изменяет положение кнопки "Удалить" и показывает ее
    $('div.for_event_lines').on('mousedown', function (e) {
        let $delete = $('#delete');
        line_clicked = $(e.target);
        line_values = $(e.target).html().split('<br>');
        if (e.button === 2) {
            $delete.offset({top: e.pageY, left: e.pageX});
            $delete.fadeIn();
        }
    });

    // функция удаляющая событие по нажатию на кнопку "Удалить"
    $('#delete').on('click', function () {
        $('#description').attr("value", line_values[0]);
        $('#event_time').attr("value", line_values[1]);
        let msg = $('#pop_up_form').serialize();
        $.ajax
        ({
            method: 'POST',
            url: '/del_data/',
            data: msg
        });
        $(line_clicked).remove();
        $(this).fadeOut();
    });

    // функция, прячущая кнопку "Удалить"
    $body.on('mousedown', function (e) {
        if (e.button !== 2 || e.target.className !== 'for_event_lines')
            $('#delete').fadeOut();
    });

    // отключение контекстного меню (чтобы не мешало при нажатии)
    $body.on('contextmenu', function () {
        return false;
    });
    // в этом блоке - удаление события из таблицы-ежедневника
});
