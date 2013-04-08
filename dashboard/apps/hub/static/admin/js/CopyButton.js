/**
 * Copy Button modeled on Add button features from Django admin and Grappelli inlines.js
 */

var OPELEC = OPELEC || function() {};

OPELEC.inlines = {

    copy: function(copy_anchor) {
        // Get stacked inline container from copy button that was clicked
        var inline = grp.jQuery(copy_anchor).closest('div'),
            inlines_div = grp.jQuery(copy_anchor).closest('.grp-group'),
            prefix = OPELEC.inlines.getFormPrefix(inlines_div),
            empty_template = inlines_div.find("#" + prefix + "-empty"),
            meta = OPELEC.inlines.getInlinesAndFormMeta(inlines_div);

        var inline_copy = inline.clone();

        // Fix h3 text
        var header = inline_copy.find('h3');
        var new_header = header.text().split(/\d{4}/)[0].trim();
        header.text(new_header);

        var orig_idx = parseInt(inline_copy.attr('id').split(prefix)[1], 10),
            to_replace = prefix + '-' + orig_idx.toString(),
            replacement = prefix + '-' + meta.totalFormsCount.toString();

        // Insert inline into DOM
        inline_copy.insertBefore(empty_template);

        // Update index in form ids
        OPELEC.inlines.updateFormIndexes(inline_copy, to_replace, replacement);

        // Update Total Forms count
        meta.totalForms.val(meta.totalFormsCount + 1);

        // Insert inline into DOM
        inline_copy.insertBefore(empty_template);

        // Re-init some grappelli initializers and edge-case handling 
        // datepicker (explained below)
        grappelli.updateSelectFilter(inline_copy);

        var options = {
            //appendText: '(mm/dd/yyyy)',
            showOn: 'button',
            buttonImageOnly: false,
            buttonText: '',
            dateFormat: grappelli.getFormat('date'),
            showButtonPanel: true,
            showAnim: '',
            // HACK: sets the current instance to a global var.
            // needed to actually select today if the today-button is clicked.
            // see onClick handler for ".ui-datepicker-current"
            beforeShow: function(year, month, inst) {
                grappelli.datepicker_instance = this;
            }
        };
        // Reinitialize datepicker, due to issue described here:
        // http://stackoverflow.com/questions/2441061/problem-when-cloning-jquery-ui-datepicker
        var dateFields = inline_copy.find('.vDateField');
        dateFields.removeClass('hasDatepicker')
                  .removeData('datepicker')
                  .unbind()
                  .datepicker(options);
        dateFields.each(function() {
            var buttons = grp.jQuery(this).siblings('.ui-datepicker-trigger');
            if (buttons.length > 1) {
                buttons.eq(1).remove();
            };
        });
        inline_copy.grp_collapsible();
        inline_copy.find('.grp-collapse').grp_collapsible();
        //TODO: restore delete handler
        //TODO: fix format M2M
        // Re-initialize copy handler
        inline_copy.find('a.grp-copy-handler').click(function(e) {
            var target = e.target;
            var target = (e.target) ? e.target : e.srcElement;
            OPELEC.inlines.copy(target);
        });
    },
    getInlinesAndFormMeta: function(inlines_div) {
        var prefix = OPELEC.inlines.getFormPrefix(inlines_div);
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
            var node = grp.jQuery(this),
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
