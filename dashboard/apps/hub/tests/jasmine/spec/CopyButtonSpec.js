describe("AdminJS", function() {
  //beforeEach(function() {
  //  player = new Player();
  //  song = new Song();
  //});
    describe("Copy button", function() {
        var copy_anchor,
            inlines_div;

        beforeEach(function() {
            loadFixtures('elec_inlines.html');
            copy_anchor = $('#elecdata_set0').find('ul > li > a')[1];
            inlines_div = $('#elecdata_set-group');
        });

        afterEach(function() {
            $('#elecdata_set-group').remove();
        });

        it("should create inline copy after pre-existing inlines", function() {
            OPELEC.copy(copy_anchor);
            var penultimate = inlines_div.find('.grp-empty-form').prev().prev();
            expect(penultimate.attr('id')).toEqual('elecdata_set1');
        });

        it("should create inline copy before empty add form template", function() {
            OPELEC.copy(copy_anchor);
            var clone = inlines_div.find('.grp-empty-form').prev();
            expect(clone.attr('id')).toEqual('elecdata_set2');
        });

        it("should increment Total Forms count", function() {
            OPELEC.copy(copy_anchor);
            var totalForms = inlines_div.find("#id_elecdata_set-TOTAL_FORMS");
            expect(totalForms.val()).toEqual('3');
        });

        describe("getInlinesAndFormMeta", function() {

            it("should return inline objs and form meta", function() {
                var inlines_div = $('#elecdata_set-group');
                var meta = OPELEC.getInlinesAndFormMeta(inlines_div);
                expect(meta.inlines.children()[0].id).toEqual('elecdata_set0');
                expect(meta.totalForms.attr('id')).toEqual('id_elecdata_set-TOTAL_FORMS');
                expect(meta.totalFormsCount).toEqual(2);
                expect(meta.maxForms.attr('id')).toEqual('id_elecdata_set-MAX_NUM_FORMS');
                expect(isNaN(meta.maxFormsCount)).toEqual(true);
            });

        });

        describe("updateFormIndexes", function() {
            var copy_anchor,
                inline_copy;

            beforeEach(function() {
                copy_anchor = $('#elecdata_set0').find('ul > li > a')[1];
                inline_copy = $(copy_anchor).closest('div').clone(true);
            })

            it("should replace indexes of form elements", function() {
                OPELEC.updateFormIndexes(inline_copy, 'elecdata_set-0','elecdata_set-1');
                expect(inline_copy.find(':input').attr('id')).toContain('elecdata_set-1');
            });

            it("should replace index of inline's container div", function() {
                // Container div does not have a dash
                OPELEC.updateFormIndexes(inline_copy, 'elecdata_set-0','elecdata_set-1');
                expect(inline_copy.attr('id')).toEqual('elecdata_set1');
            });
        });
    });// end Copy Button tests
});
