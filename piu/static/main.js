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
        if (!$('#text').val()) { return; }
        $('form').submit();
    });
    shortcut.add('ctrl+j', function() { lexers.focus(); });
    shortcut.add('ctrl+n', function() { document.location.href = '/'; });

    // links do not work with selections
    $('.linenos a').each(function() {
        this.rel = this.href.split('#')[1];
        this.removeAttribute('href');
    });

    hlter.run();

    // highlight hovered lines
    $('.line').hover(
        function() { $(this).addClass('over'); },
        function() { $(this).removeClass('over'); }
        );
    $('.linenos a').hover(
        function() { $('#' + this.rel).addClass('over'); },
        function() { $('#' + this.rel).removeClass('over'); }
        );

});

hlter = {
    last_location: null,
    // if user is selecting lines, first line
    selecting: null,
    // if ctrl or shift is pressed
    shift: false,
    ctrl: false,
    // time in ms that the URL is queried for changes
    run_interval_every: 50,

    run: function() {
        var app = this;
        this.check();
        this._interval = setInterval(function() {
            app.check.apply(app);
        }, this.run_interval_every);

        $('.linenos a').disableTextSelect();

        $('.linenos a').mousedown(function() { app.selecting = this.rel; })
            .mouseup(function() { app.select(this.rel); app.selecting = null; });
        $('.line').mouseup(function() { app.select(this.id); app.selecting = null; });

        $(window).keydown(function(event) {
            if (event.keyCode == 16) { app.shift = true; }
            else if (event.keyCode == 17) { app.ctrl = true; }
        }).keyup(function(event) {
            if (event.keyCode == 16) { app.shift = false; }
            else if (event.keyCode == 17) { app.ctrl = false; }
        });
    },

    select: function(end) {
        if (!this.selecting) { return; }
        var range;

        if (end && end != this.selecting)
            { range = this.selecting + ':' + end; }
        else
            { range = this.selecting; }

        if ((this.ctrl || this.shift) && window.location.hash)
            { window.location.hash += ',' + range; }
        else
            { window.location.hash = range; }
    },

    perform: function() {
        $('.line').removeClass('selected');
        var specifiers = this.location().split(',');

        for (k in specifiers) { if (specifiers.hasOwnProperty(k)) {
            var pair = specifiers[k].split(':');
            if (pair.length != 2)
                { pair[1] = pair[0]; }

            start = this.int(pair[0]); end = this.int(pair[1]);
            if (start > end)
                { end = (start += end -= start) - end; } // swap variables

            for (i = start; i <= end; i += 1) {
                $('#l-' + i).addClass('selected');
            } }
        }
    },

    int: function(s) {
        return parseInt(s.split('-')[1], 10);
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
    }
};

/* .disableTextSelect, version 1.2
   Copyright (c) 2007 James Dempster
   Copyright (c) 2009 Alexander Solovyov
   under terms of MIT License
 */
(function($) {
    if ($.browser.mozilla) {
        $.fn.disableTextSelect = function() {
            return this.each(function() { $(this).css({'MozUserSelect' : 'none'}); });
        };
        $.fn.enableTextSelect = function() {
            return this.each(function() { $(this).css({'MozUserSelect' : ''}); });
        };
    } else {
        var tgt = ($.browser.msie ? 'selectstart' : 'mousedown')+'.disableTextSelect';
        $.fn.disableTextSelect = function() {
            return this.each(function() {
                $(this).bind(tgt, function() { return false; });
            });
        };
        $.fn.enableTextSelect = function() {
            return this.each(function() { $(this).unbind(tgt); });
        };
    }
})(jQuery);
