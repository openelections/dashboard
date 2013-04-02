(function($) {
    $(document).ready(function() {
        $('a.grp-copy-handler').each(function() {

            // Unbind the original click event?
            $(this).click(function(e) {
                var target = (e.target) ? e.target : e.srcElement;
                OPELEC.inlines.copy(target);
            });
       });
    });
})(grp.jQuery);
