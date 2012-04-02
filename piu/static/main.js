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

    hlter.run();

    // highlight hovered lines
    $('.line').hover(
        function() { $('#' + this.id).addClass('over'); },
        function() { $('#' + this.id).removeClass('over'); }
        );
    $('.linenos a').hover(
        function() { $('#' + this.rel).addClass('over'); },
        function() { $('#' + this.rel).removeClass('over'); }
        );
});

hlter = {
    last_location: null,    // which location we're following right now
    run_interval_every: 50, // time in ms that the URL is queried for changes
    selecting: null,        // if user is selecting lines, first line
    current: null,          // current line or line number if any
    modifier: 0,            // if ctrl or shift is pressed
    // shift - 16, ctrl - 17
    isModifier: function(code) { return [16].indexOf(code) + 1; },
    bit: function(code) { return 1 << (code - 16); },

    run: function() {
        var app = this;
        this.lineselection(true);
        // this.check();
        this._interval = setInterval(function() {
            app.check.apply(app);
        }, this.run_interval_every);

        $('.linenos a').disableTextSelect();

        $('.linenos a')
            .mousedown(function(e) { if (e.which == 1) app.selectStart(this.rel); })
            .mouseup(function() { app.selectEnd(this.rel); });
        $('.line').mouseup(function() { app.selectEnd(this.id); });

        $('.line').mousemove(function() { app.current = this.id; });
        $('.linenos a').mousemove(function() { app.current = this.rel; });

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
    selectEnd: function(id) { this.select(id); },

    select: function(end) {
        if (!this.selecting) { return; }

        var range = this.selecting;
        if (end && end != this.selecting) {
            range += ':' + end;
        }

        if (this.modifier && window.location.hash) {
            window.location.hash += ',' + range;
        } else {
            window.location.hash = range;
        }

        this.selecting = null;
    },

    ongoingselection: function() {
        $('.linenos a').removeClass('selecting');
        if (!(this.selecting && this.current)) { return; }

        var range = this.range(this.selecting, this.current, '#a-');
        $(range.join(', ')).addClass('selecting');
    },

    lineselection: function(onload) {
        $('.line, .linenos a').removeClass('selected');
        var specifiers = this.location().split(',');
        var first;
        for (var i = 0, l = specifiers.length; i < l; i++) {
            var pair = this.getPair(specifiers[i]);
            var range = this.range(pair[0], pair[1]);
            $(range.join(', ')).addClass('selected');

            if (onload && (!first || first > pair[0])) {
                first = pair[0];
            }
        }

        if (onload && first !== undefined) {
            $('html').scrollTop($('#' + first).offset().top);
        }
    },

    int: function(v) { return parseInt(v, 10); },

    getPair: function(x) {
        var pair = $.map(x.split(':'), this.int);
        if (pair[0] > pair[1]) {
            return [pair[1], pair[0]];
        }
        return pair;
    },

    range: function(start, end, prefix) {
        if (!start) { return []; }
        if (!end) { end = start; }
        if (!prefix) { prefix = '#'; }

        var range = [];
        for (var i = start; i <= end; i++) {
            range.push(prefix + i);
        }
        return range;
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
