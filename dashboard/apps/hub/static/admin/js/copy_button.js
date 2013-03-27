/**
 * Copy Button modeled on GRAPPELLI INLINES js
 * jquery-plugin for inlines (stacked and tabular)
 */

(function($) {
    $.fn.django_inline_exts = function(options) {
        var defaults = {
            prefix: "form",                         // The form prefix for your django formset
            copyText: "Create copy from this record",      // Text for the copy link
            addCssClass: "grp-add-handler",           // CSS class applied to the add link
            copyCssClass: "grp-copy-handler",           // CSS class applied to the copy link
            emptyCssClass: "grp-empty-form",            // CSS class applied to the empty row
            formCssClass: "grp-dynamic-form"           // CSS class applied to each form in a formset
        };
        options = $.extend(defaults, options);
        
        return this.each(function() {
            var inline = $(this); // the current inline node
            var totalForms = inline.find("#id_" + options.prefix + "-TOTAL_FORMS");
            // set autocomplete to off in order to prevent the browser from keeping the current value after reload
            //totalForms.attr("autocomplete", "off");
            // init inline and add-buttons
            //console.log("THIS WORKED");
            //initInlineForms(inline, options);
            initCopyButtons(inline, options);
            // button handlers
            copyButtonHandler(inline.find("a." + options.copyCssClass), options);
        });
    };
    
    updateFormIndex = function(elem, options, replace_regex, replace_with) {
        elem.find(':input,span,table,iframe,label,a,ul,p,img').each(function() {
            var node = $(this),
                node_id = node.attr('id'),
                node_name = node.attr('name'),
                node_for = node.attr('for'),
                node_href = node.attr("href");
            if (node_id) { node.attr('id', node_id.replace(replace_regex, replace_with)); }
            if (node_name) { node.attr('name', node_name.replace(replace_regex, replace_with)); }
            if (node_for) { node.attr('for', node_for.replace(replace_regex, replace_with)); }
            if (node_href) { node.attr('href', node_href.replace(replace_regex, replace_with)); }
        });
    };
    /**    
    initInlineForms = function(elem, options) {
        elem.find("div.grp-module").each(function() {
            var form = $(this);
            // add options.formCssClass to all forms in the inline
            // except table/theader/add-item
            if (form.attr('id') !== "") {
                form.not("." + options.emptyCssClass).not(".grp-table").not(".grp-thead").not(".add-item").addClass(options.formCssClass);
            }
        });
    };
    */
    
    initCopyButtons = function(elem, options) {
        var totalForms = elem.find("#id_" + options.prefix + "-TOTAL_FORMS");
        var maxForms = elem.find("#id_" + options.prefix + "-MAX_NUM_FORMS");
        //var addButtons = elem.find("a." + options.addCssClass);
        var copyButtons = elem.find("a." + options.copyCssClass);
    };
    
    copyButtonHandler = function(elem, options) {
        elem.bind("click", function() {
            var inline = elem.parents(".grp-group"),
                totalForms = inline.find("#id_" + options.prefix + "-TOTAL_FORMS"),
                maxForms = inline.find("#id_" + options.prefix + "-MAX_NUM_FORMS"),
                addButtons = inline.find("a." + options.addCssClass),
                empty_template = inline.find("#" + options.prefix + "-empty");

            // create new form
            var index = parseInt(totalForms.val(), 10),
                form = elem.clone(true);
            //form.removeClass(options.emptyCssClass)
            //    .attr("id", empty_template.attr('id').replace("-empty", index))
            //    .insertBefore(empty_template)
            //    .addClass(options.formCssClass);

            //var index = parseInt(totalForms.val(), 10),
            //    form = empty_template.clone(true);
            //form.removeClass(options.emptyCssClass)
            //    .attr("id", empty_template.attr('id').replace("-empty", index))
            //    .insertBefore(empty_template)
            //    .addClass(options.formCssClass);
            // update form index
            var re = /__prefix__/g;
            updateFormIndex(form, options, re, index);
            // update total forms
            totalForms.val(index + 1);
        });
    };
        
})(grp.jQuery);
