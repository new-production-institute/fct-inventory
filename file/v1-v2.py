#!/usr/bin/env python3

import toml
#
# read v1
#
v1 = toml.load("inv.toml")
#
# create v2
#
v2 = {}
#
# purposes
#
v2['purposes'] = {}
for subject in v1['topics']:
   topic = v1['topics'][subject]
   v2['purposes'][subject] = {}
   v2['purposes'][subject]['program'] = ['Fab Academy']
   v2['purposes'][subject]['URL'] = ['https://www.fabacademy.org']
#
# sources
#
v2['sources'] = {}
for subject in v1['topics']:
   topic = v1['topics'][subject]
   for vendor in topic['sources']:
      source = topic['sources'][vendor]
      v2['sources'][vendor] = {}
      v2['sources'][vendor]['URL'] = [topic['sources'][vendor]['URL']]
      v2['sources'][vendor]['currency'] = [topic['sources'][vendor]['currency']]
      v2['sources'][vendor]['currency_symbol'] = ['$']
#
# items
#
v2['items'] = []
for subject in v1['topics']:
   topic = v1['topics'][subject]
   for vendor in topic['sources']:
      source = topic['sources'][vendor]
      for category in source['categories']:
         items = source['categories'][category]
         for item in items:
            v2['items'].append({})
            v2['items'][-1]['purpose'] = [subject]
            v2['items'][-1]['source'] = [vendor]
            v2['items'][-1]['category'] = [category]
            if 'description' in item.keys():
               v2['items'][-1]['description'] = [item['description']]
            else:
               v2['items'][-1]['description'] = []
            if 'item' in item.keys():
               v2['items'][-1]['item'] = [item['item']]
            else:
               v2['items'][-1]['item'] = []
            if 'URL' in item.keys():
               v2['items'][-1]['URL'] = [item['URL']]
            else:
               v2['items'][-1]['URL'] = []
            if 'manufacturer' in item.keys():
               v2['items'][-1]['manufacturer'] = [item['manufacturer']]
            else:
               v2['items'][-1]['manufacturer'] = []
            if 'price' in item.keys():
               v2['items'][-1]['price'] = [item['price']]
            else:
               v2['items'][-1]['price'] = []
            if 'quantity' in item.keys():
               v2['items'][-1]['quantity'] = [item['quantity']]
            else:
               v2['items'][-1]['quantity'] = []
            v2['items'][-1]['attributes'] = ['active']

#
# write v2
#
f = open("inv2.toml","w")
toml.dump(v2,f)
f.close()
