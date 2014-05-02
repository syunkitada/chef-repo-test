name 'mysql'
description 'mysql server'

run_list 'recipe[mysql::server]'

override_attributes(
    'mysql' => {
        'version' => '5.5',
        'server_root_password' => 'pass'
    }
)

