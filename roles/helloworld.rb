name "helloworld"
description "helloworld role applied to all nodes."

run_list "recipe[helloworld]",
         "recipe[helloworld2]"

override_attributes(
    "helloworld" => {
        "message" => "welcome role!"
    }
)


