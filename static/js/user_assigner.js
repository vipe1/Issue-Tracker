$(document).ready(function() {
    $('.user-assigner').click(function() {
        const form = $(this.parentNode.parentNode)
        const new_assignee = $(this).data('new-assignee')

        $('<input>', {
            type: 'hidden',
            name: 'new_assignee',
            value: new_assignee
        }).appendTo(form)
        $(form).submit()
    })
})