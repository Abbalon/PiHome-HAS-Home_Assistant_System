//Define el comportamiento de los botones que están relacionados con las acciones de los dispositivos
$(function () {
    $('.action > a').bind('click', function () {
        let $this = $(this),
            $req = $this.attr('target');

        //Realizamos la petición al servidor
        $.getJSON($req, function (data) {
            // Definimos cual será el comportamiento cuando el servidor nos responda
            console.log(data.status);
        })
            .done(function (data) {
                console.log("DONE: " + data.status);
            })
            .fail(function (data) {
                console.log("FAIL: " + data);
            })
            .always(function () {
                return false;
            });
    });
});
