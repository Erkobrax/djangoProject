$('#search-form').submit(function(event) {
    $.post('/search/', $(this).serialize(), function(data) {
        $('.posts').html(data);
    });
    event.preventDefault();
});