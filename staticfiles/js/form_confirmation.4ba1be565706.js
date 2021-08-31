$(document).ready(function (e){
    $('.form-confirmation').one('submit', function (e){
        e.preventDefault()
        if(confirm('Are you sure you want to do it?')){
            $(this).submit()
        }
    })
})