# my_pb
itty bitty pb


Clone to /opt/

Apache Conf: (configure to make it work for you of course)
```
<VirtualHost *:80>
    ServerName server_name_here

    WSGIDaemonProcess util threads=5 home=/opt/my_pb/
    WSGIScriptAlias / "/opt/my_pb/util.wsgi"

    <Directory "/opt/my_pb">
        Options Indexes FollowSymLinks MultiViews ExecCGI
        AllowOverride None
        Require all granted
        WSGIProcessGroup util
        WSGIApplicationGroup %{GLOBAL}
    </Directory>

ErrorLog "/var/log/apache2/pb_error.log"
LogLevel info
CustomLog "/var/log/apache2/pb_access.log" "combined"
</VirtualHost>
```
