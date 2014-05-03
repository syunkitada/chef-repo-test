# mysql fabscript

master-slaveを利用するには、my.confにlog-binとserver-idを事前に設定する。
``` bash
[mysqld]
log-bin
server-id = <num>
```

mysql> SHOW SLAVE STATUS;
Slave_IO_Running: Yes
Slave_SQL_Running: Yes

トラブルシューティング
Last_IO_Error: error connecting to master 'masterslave@192.168.254.129:3306' - retry-time: 60  retries: 86400

ネットワークの問題なので
マスタのを見て確認
/etc/iptables

$ fab mysql.setdata mysql.setup_user mysql.dump_master mysql.setup_slave mysql.show_slave_status
```
