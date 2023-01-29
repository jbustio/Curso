odoo.define('applicant.dynamic.snippet', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');

    publicWidget.registry.books = publicWidget.Widget.extend({
        selector: '.book_snippet',
        disabledInEditableMode: false,
        start: function () {
            var self = this;
            var rows = this.$el[0].dataset.numberOfBooks || '5';
            this.$el.find('td').parents('tr').remove();
            this._rpc({
                model: 'hr.applicant',
                method: 'search_read',
                domain: [],
                fields: ['partner_name', 'full_skills_levels'],
                orderBy: [{name: 'create_date', asc: false}],
                limit: parseInt(rows)
            }).then(function (data) {
                _.each(data, function (applicant) {
                    self.$el.append(
                        $('<tr />').append(
                            $('<td />').text(applicant.partner_name),
                            $('<td />').text(applicant.full_skills_levels),
                        ));
                });
            });
        },
    });
});