db.createUser(
    {
        user    : "home-automation",
        pwd     : "home-automation",
        roles   : [
            {
                role: "readWrite",
                db  : "home-automation"
            }
        ]    
    }
)