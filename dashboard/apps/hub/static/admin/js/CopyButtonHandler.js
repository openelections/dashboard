(function($) {
    $(document).ready(function() {
        $('a.grp-copy-handler').each(function() {
            $(this).click(function(e) { OPELEC.inlines.copy(e.target);});
        });
    });
})(grp.jQuery);
