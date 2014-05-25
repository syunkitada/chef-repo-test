name "sensu"
description "this is sensu role"

run_list "sensu",
         "sensu::redis",
         "sensu::rabbitmq"

