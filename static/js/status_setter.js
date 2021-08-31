$(document).ready(function() {
    $('.status-setter').click(function() {
        const form = $(this.parentNode.parentNode)
        const new_status = $(this).data('new-status')

        $('<input>', {
            type: 'hidden',
            name: 'new_status',
            value: new_status
        }).appendTo(form)
        $(form).submit()
    })
})