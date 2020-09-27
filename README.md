# TFG

## Creación del WebApp como un servicio
### Systemd
Configuramos el fichero para añadir a Systemd en `/config/PiHome.service`
Para ello nos basamos en [este tutorial](https://www.golinuxcloud.com/run-systemd-service-specific-user-group-linux/ "Creación de un usuario para el servicio")
y en [este otro](https://blog.miguelgrinberg.com/post/running-a-flask-application-as-a-service-with-systemd "Para la configuración del servicio")

#### Creación de un usuario específico
1. Creación del usuario y asignación de su contraseña

        $ useradd -c "User for PiHome.service" pi_home
        $ passwd pi_home <pass>
1. Comprobación del resultado  

        $ id pi_home
        $ ls -la /home/pi_home/
        $ grep pi_home /etc/passwd
1. Recargar Systemd  
Una vez que hemos creado el `.service` y movido a `/etc/systemd/system`, recargamos el listado de servicios disponibles:  
  
        $  systemctl daemon-reload
1. Habilitamos el service nuevo  

        $ systemctl enable PiHome.service
1. Comprobamos el resultado  

        $ systemctl restart PiHome.service
        $ systemctl status PiHome.service
        $ ps -ef | grep PiHome