$(document).ready(function() {

        $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/suggest_category/', {suggestion: query}, function(data){
         $('#location_suggestion_list').html(data);
        });
    });
});