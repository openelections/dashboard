/**
 * Copy Button modeled on Add button features from Django admin and Grappelli inlines.js
 */

//(function($) {
//    $.fn.admin_inline_exts = function(options) {
//window.ELEX = window.ELEX || {}
    var OPELEC = {
        copy: function(copy_anchor) {
            // Get stacked inline container from copy button that was clicked
            var inline = $(copy_anchor).closest('div'),
                inlines_div = $(copy_anchor).closest('.grp-group'),
                prefix = this.getFormPrefix(inlines_div),
                empty_template = inlines_div.find("#" + prefix + "-empty");

            // Upddate form indexes
            var meta = this.getInlinesAndFormMeta(inlines_div);

            // Clone the element and update its indexes
            var inline_copy = inline.clone(true);

            var orig_idx = parseInt(inline_copy.attr('id').split(prefix)[1], 10),
                to_replace = prefix + '-' + orig_idx.toString(),
                replacement = prefix + '-' + meta.totalFormsCount.toString();

            // Update ids in forms which have a dash (e.g. elecdata_set-0)
            this.updateFormIndexes(inline_copy, to_replace, replacement);

            // Update Total Forms count
            meta.totalForms.val(meta.totalFormsCount + 1);

            // Insert inline into DOM
            inline_copy.insertBefore(empty_template);

        },
        getInlinesAndFormMeta: function(inlines_div) {
            var prefix = this.getFormPrefix(inlines_div);
            var inlines = inlines_div.find(".grp-items");
            var totalForms = inlines_div.find("#id_" + prefix + "-TOTAL_FORMS");
            var maxForms = inlines_div.find("#id_" + prefix + "-MAX_NUM_FORMS");

           return {
            'inlines':inlines,
            'totalForms':totalForms,
            'totalFormsCount':parseInt(totalForms.val(), 10),
            'maxForms':maxForms,
            'maxFormsCount':parseInt(maxForms.val(), 10)
           };
        },
        getFormPrefix: function(inlines_div) {
            return inlines_div[0].id.split('-')[0];
        },
        updateFormIndexes: function(elem, replace_regex, replace_with) {
            elem.find(':input,span,table,iframe,label,a,ul,p,img,div').each(function() {
                var node = $(this),
                    node_id = node.attr('id'),
                    node_name = node.attr('name'),
                    node_for = node.attr('for'),
                    node_href = node.attr("href"),
                    node_class = node.attr("class");
                if (node_id) { node.attr('id', node_id.replace(replace_regex, replace_with)); }
                if (node_name) { node.attr('name', node_name.replace(replace_regex, replace_with)); }
                if (node_for) { node.attr('for', node_for.replace(replace_regex, replace_with)); }
                if (node_href) { node.attr('href', node_href.replace(replace_regex, replace_with)); }
                if (node_class) { node.attr('class', node_class.replace(replace_regex, replace_with)); }
            });

            // Fix parent div's id which does not have a dash (e.g. elecdata_set0)
            var old_id = replace_regex.replace('-',''),
                new_id = replace_with.replace('-','')
                div_id = elem.attr('id');
            elem.attr('id', div_id.replace(old_id, new_id));
        }
    };

/*
django.jQuery(document).ready(function($) {
    $('.grp-copy-handler').each(function(elemIndex) {
        var copy_btn = $(this);
        //console.log(copy_link.text());
        inline.bind("click", OPELEC.copy);
    });
});
//})(grp.jQuery);
*/
