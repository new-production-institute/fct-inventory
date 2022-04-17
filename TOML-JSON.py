#!/usr/bin/env python3

import toml,json
#
# read TOML
#
data = toml.load("public/inv.toml")
#
# write JSON
#
f = open("public/inv.json","w")
json.dump(data,f)
f.close()
