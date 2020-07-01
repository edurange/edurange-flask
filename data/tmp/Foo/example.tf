variable "students" {
                     type = list(object({
                         login              = string,
                        password           = object({ plaintext = string, hash = string }),
                         variables          = object({
                             follow_me_filename = string,
                             super_secret       = string
                          })
                            }))
                         description = "list of players"
                         default = []
                }