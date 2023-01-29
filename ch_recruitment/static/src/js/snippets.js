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
                fields: ['partner_name', 'display_name', 'full_skills_levels'],
                orderBy: [{name: 'create_date', asc: false}],
                limit: parseInt(rows)
            }).then(function (data) {

                _.each(data, function (applicant) {

                    var container = $('<div></div>')

                    _.each(applicant.full_skills_levels.split(','), (val) => {
                        var badge = $(`<span class="badge rounded-pill bg-light text-dark">${val}</span>`)
                        container.append(badge)
                    })
                    var name = applicant.partner_name || applicant.display_name;
                    var name_label = $(`<div><h4>${name}</h4></div>`)
                    if (applicant.partner_name)
                        name_label = name_label.append($(`<small class="text-bold">${applicant.display_name}</small>`))

                    self.$el.append(
                        $('<tr />').append(
                            $('<td />').append(name_label),
                            $('<td />').append(container),
                        ));
                });
            });
        },
    });
});