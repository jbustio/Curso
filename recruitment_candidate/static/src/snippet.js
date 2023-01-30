odoo.define('candidate.dynamic.snippet',function(require){
    'use strict'
     var publicWidget = require('web.public.widget');
     
     
     publicWidget.registry.candidates = publicWidget.Widget.extend({
        selector:'.candidate_snippet',
        disableInEditableMode: false,
        start:function(){
            var self = this;
            var rows = this.$el[0].dataset.numberOfCandidates||'5';
            this.$el.find('td').parents('tr').remove()
            this._rpc({
                model:'recruitment.candidate',
                method:'search_read',
                domain:[],
                fields:['name','dev_skill.name'],
                orderBy:[{name:'dev_skill.years_experience',asc:false}],
                limit:parseInt(rows)
            }).then(function(data){
                _.each(data,function(candidate){
                    self.$el.append(
                        $('<tr/>').append(
                            $('<td/>').text(candidate.name),
                            $('<td/>').text(candidate.lastname)
                        ));
                });
            });
        },
     });
});