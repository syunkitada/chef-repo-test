name "helloworld"
description "helloworld role applied to all nodes."

run_list "recipe[helloworld]"

override_attributes(
    "helloworld" => {
        "message" => "welcome role!"
    }
)


