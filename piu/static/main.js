// finding out keyCode:
// http://www.cambiaresearch.com/articles/15/javascript-char-codes-key-codes

function addShortcut(keyCode, mods, callback) {
    mods = mods || {};
    document.addEventListener('keydown', function(e) {
        var modsMatched = ((e.ctrlKey  == !!mods.ctrl) &&
                           (e.shiftKey == !!mods.shift) &&
                           (e.altKey   == !!mods.alt) &&
                           (e.metaKey  == !!mods.meta));
        var received = e.keyCode !== undefined ? e.keyCode : e.which;
        if (modsMatched && received == keyCode) {
            callback(e);
            e.preventDefault();
        }
    });
}

$(document).ready(function() {
    var lexers = $('#lexers');
    var text = $('#text');

    lexers.change(function() {
        $('.hot.selected').removeClass('selected');
        $('.hot[rel=' + lexers.val() + ']').addClass('selected');
    });

    $('span.hot').click(function() {
        lexers.val($(this).attr('rel')).change();
        text.focus();
    });

    $('#wrap').click(function(e) {
        e.preventDefault();
        $('html').toggleClass('wrap');
    });

    lexers.change();

    // resize textarea to fill maximum area without adding a scrollbar
    var newheight = $(window).height() - $('html').height() + text.height();
    if (newheight > text.height())
        text.height(newheight);

    addShortcut(13, {ctrl: true}, function(e) { // ctrl+enter
        if (!$('#text').val()) { return; }
        $('form').submit();
    });
    addShortcut(74, {ctrl: true}, function() { // ctrl+j
        lexers.focus();
    });
    addShortcut(78, {ctrl: true}, function() { // ctrl+n
        document.location.href = '/';
    });

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

        if (onload && first) {
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

/* .disableTextSelect, version 2.0
   Copyright (c) 2007 James Dempster
   Copyright (c) 2009, 2015 Alexander Solovyov
   under terms of MIT License
 */
(function($) {
    if (navigator.userAgent.match(/msie/)) {
        $.fn.disableTextSelect = function() {
            return this.each(function() {
                $(this).bind('selectstart', function(e) { e.preventDefault(); });
            });
        };
        $.fn.enableTextSelect = function() {
            return this.each(function() { $(this).unbind('selectstart'); });
        };
    } else {
        // handled through css, search for user-select
        $.fn.disableTextSelect = function() {};
        $.fn.enableTextSelect = function() {};
    }
})(jQuery);
