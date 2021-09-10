$(document).ready(function() {
    let sort_url = ''
    $('.srt').click(function() {
        if ($('.form-check-input:checked').val() == 'desc') sort_url = '-'
        sort_url += $(this).data('sorter')

        const queries = {}
        queries['sort']=sort_url

        document.location.href="?"+$.param(queries)
    })
})