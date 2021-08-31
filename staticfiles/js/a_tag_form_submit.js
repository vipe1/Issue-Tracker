$(document).ready(function() {
    $('.a-tag-form-submit').click(function() {
        const form = $(this).parents('form')
        $(form).submit()
    })
})