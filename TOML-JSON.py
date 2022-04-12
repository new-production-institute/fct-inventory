#!/usr/bin/env python3

import toml,json

data = toml.load("public/inv.toml")
f = open("public/inv.json","w")
json.dump(data,f)
f.close()
