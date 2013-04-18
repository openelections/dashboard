(function($) {
    $(document).ready(function() {
        $('a.grp-copy-handler').each(function() {

            $(this).click(function(e) {
                var target = (e.target) ? e.target : e.srcElement;
                OPELEC.inlines.copy(target);
            });
       });
    });
})(grp.jQuery);
