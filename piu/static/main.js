$(document).ready(function() {
    var lexers = $('#id-lexer');
    $('span.hot').click(function() {
        var lang = $(this).attr('rel');
        $('#id-lexer [value=' + lang + ']').attr('selected', 1);
        });
    });
