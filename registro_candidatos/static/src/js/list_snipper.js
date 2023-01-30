odoo.define("registro_candidatos.dynamic.snippet", ["web.ajax"], function (require) {
    "use strict";
    var ajax = require("web.ajax");
    $(document).ready(function () {
        var container = document.getElementById("list-row");
        if (container) {
            container.innerHTML = "";
            container.innerHTML = "<div class='col text-center'>Cargando ...</div>";

            ajax.jsonRpc("/list_candidate_tech", "call", {}).then(function (data) {
                container.innerHTML = "";
                console.log(data);
                for (var i = 0; i < data.length; i++){
                    container.innerHTML +=
                        "<div class='mt-4'>" +
                            "<dl>" +
                                "<dt>"+JSON.stringify(data[i].candidate_id[1])+"</dt>" +
                                    "<dd>"+JSON.stringify(data[i].tech_id[1])+"</dd>"+
                                    "<dd>"+JSON.stringify(data[i].experience)+"</dd>" +
                            "</dl>" +
                        "</div>";
                }
            })
        }
    });
    }
);
