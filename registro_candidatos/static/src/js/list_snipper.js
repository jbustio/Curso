odoo.define('registro_candidatos.list.snippets', ["web.ajax"], function (require) {
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
                container.innerHTML += "<div><h6>data[i]</h6></div>"
            })
        }
    });
    }
);
