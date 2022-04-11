#!/usr/bin/env python3

import toml,json

data = toml.load("inv.toml")
f = open("inv.json","w")
json.dump(data,f)
f.close()
