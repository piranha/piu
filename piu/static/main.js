$(document).ready(function() {
    var lexers = $('#lexers');
    var text = $('#text');

    lexers.change(function() {
        $('.hot').removeClass('selected');
        $('.hot[rel=' + lexers.val() + ']').addClass('selected');
    });

    $('span.hot').click(function() {
        lexers.val($(this).attr('rel')).change();
        text.focus();
    });

    lexers.change();

    // resize textarea to fill maximum area without adding a scrollbar
    var newheight = $(window).height() - $('html').height() + text.height();
    if (newheight > text.height())
        text.height(newheight);

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
        function() { $(line(this.id)).addClass('over'); },
        function() { $(line(this.id)).removeClass('over'); }
        );
    $('.linenos a').hover(
        function() { $(line(this.rel)).addClass('over'); },
        function() { $(line(this.rel)).removeClass('over'); }
        );

});

function line(id) {
    if (id.toString().indexOf('-') + 1) { // that's l-num
        return '#' + id + ', .linenos a[rel=' + id + ']';
    } else {
        return '#l-' + id + ', .linenos a[rel=l-' + id + ']';
    }
};

hlter = {
    last_location: null,    // what location we're following right now
    run_interval_every: 50, // time in ms that the URL is queried for changes
    selecting: null,        // if user is selecting lines, first line
    current: null,          // current line or line number if any
    modifier: 0,            // if ctrl or shift is pressed
    // ctrl - 16, shift - 17
    isModifier: function(code) { return [16,17].indexOf(code) + 1; },
    bit: function(code) { return 1 << (code - 16); },

    run: function() {
        var app = this;
        this.check();
        this._interval = setInterval(function() {
            app.check.apply(app);
        }, this.run_interval_every);

        $('.linenos a').disableTextSelect();

        $('.linenos a').mousedown(function() { app.selectStart(this.rel); })
            .mouseup(function() { app.selectEnd(this.rel); });
        $('.line').mouseup(function() { app.selectEnd(this.id); });

        // $('.line, .linenos a').mouseenter(function() { app.current = this; })
        //     .mouseleave(function() { if (app.current == this) { app.current = null; } });
        $('.line').mousemove(function() { app.current = this.id; })
        $('.linenos a').mousemove(function() { app.current = this.rel; })

        // yay bitwise :P
        $(window).keydown(function(event) {
            if (app.isModifier(event.keyCode)) {
                app.modifier |= app.bit(event.keyCode);
            }
        }).keyup(function(event) {
            if (app.isModifier(event.keyCode)) {
                app.modifier ^= app.bit(event.keyCode);
            }
        });
    },

    selectStart: function(id) { this.selecting = id; },
    selectEnd: function(id) { this.select(id); this.selecting = null; },

    select: function(end) {
        if (!this.selecting) { return; }

        var range = this.selecting;
        if (end && end != this.selecting)
            { range += ':' + end; }

        if (this.modifier && window.location.hash)
            { window.location.hash += ',' + range; }
        else
            { window.location.hash = range; }
    },

    ongoingselection: function() {
        $('.linenos a').removeClass('selecting');
        if (!(this.selecting && this.current)) { return; }
        var pair = this.startend([this.selecting, this.current]);

        for (var i = pair[0]; i <= pair[1]; i += 1) {
            $('.linenos a[rel=l-' + i + ']').addClass('selecting');
        }
    },

    lineselection: function() {
        $('.line, .linenos a').removeClass('selected');
        var specifiers = this.location().split(',');

        for (var k in specifiers) { if (specifiers.hasOwnProperty(k)) {
            var pair = specifiers[k].split(':');
            if (pair.length != 2)
                { pair[1] = pair[0]; }
            pair = this.startend(pair);

            for (var i = pair[0]; i <= pair[1]; i += 1) {
                $(line(i)).addClass('selected');
            }
        } }
    },

    int: function(s) {
        return parseInt(s.split('-')[1], 10);
    },

    startend: function(pair) {
        self = this;
        pair = $.map(pair, function(x) { return self.int(x); });
        if (pair[0] > pair[1])
            { return [pair[1], pair[0]]; }
        return pair;
    },

    location: function() {
        return window.location.hash.slice(1);
    },

    check: function() {
        this.ongoingselection();
        var location = this.location();
        if (location != this.last_location) {
            this.last_location = location;
            this.lineselection();
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
