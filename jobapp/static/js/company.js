$(document).ready(function(){
    $('#file_input_cover, #file_input').on('change',function(){
        $(this).closest('form').find('button[type="submit"]').addClass('bg-secondary text-white')
    })
})