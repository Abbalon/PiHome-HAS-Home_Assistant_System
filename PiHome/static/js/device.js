//Define el comportamiento de los botones que están relacionados con las acciones de los dispositivos
$(function () {
    $('.action > a').bind('click', function () {
        let $this = $(this),
            $req = $this.attr('target');

        //Realizamos la petición al servidor
        $.getJSON($req, function (data) {
            // Definimos cual será el comportamiento cuando el servidor nos responda
            console.log(data.code);
        })
            .done(function (data) {
                cod = data.code
                desc = JSON.stringify(data.description)
                msg = data.status
                if (data.code === -1) {
                    desc = ""
                    $.each(data.description, function (index, text) {
                        desc = desc + text + "\n"
                    });
                    swal(
                        "¡Cuidado!",
                        desc,
                        "warning"
                    );
                } else {
                    swal(
                        "Hecho",
                        msg,
                        "info");
                }
            })
            .fail(function (data) {
                err = data.error
                desc = JSON.stringify(data.description)
                swal(
                    err,
                    desc,
                    "error"
                )
            })
            .always(function () {
                return false;
            });
    });
});
