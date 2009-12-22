$(document).ready(function() {
    var lexers = $('#lexers');

    lexers.change(function() {
        $('.hot').removeClass('selected');
        $('.hot[rel=' + lexers.val() + ']').addClass('selected');
    });

    $('span.hot').click(function() {
        lexers.val($(this).attr('rel')).change();
        $('#text').focus();
    });

    lexers.change();

    shortcut.add('ctrl+enter', function() {
        if (!$('#text').val()) return;
        $('form').submit();
    });
    shortcut.add('ctrl+j', function() { lexers.focus(); });
    shortcut.add('ctrl+n', function() { document.location.href = '/'; });

    // highlight hovered lines
    $('.line').hover(
        function() { $(this).addClass('over'); },
        function() { $(this).removeClass('over'); }
        );
    $('.linenos a').hover(
        function() { $('#' + this.href.split('#')[1]).addClass('over'); },
        function() { $('#' + this.href.split('#')[1]).removeClass('over'); }
        );

    hlter.run();
});

hlter = {
    last_location: null,
    // time in ms that the URL is queried for changes
    run_interval_every: 50,

    run: function() {
        var app = this;
        this.check();
        this._interval = setInterval(function() {
            app.check.apply(app);
        }, this.run_interval_every);
    },

    perform: function() {
        $('.line').removeClass('selected');
        var specifiers = this.location().split(',');
        for (k in specifiers) {
            var pair = specifiers[k].split(':');
            if (!(pair.length == 2))
                pair[1] = pair[0];
            for (i = this.int(pair[0]); i <= this.int(pair[1]); i += 1) {
                $('#l-' + i).addClass('selected');
            }
        }
    },

    int: function(s) {
        return parseInt(s.split('-')[1]);
    },

    location: function() {
        return window.location.hash.slice(1);
    },

    check: function() {
        var location = this.location();
        if (location != this.last_location) {
            this.last_location = location;
            this.perform();
        }
    },
}
