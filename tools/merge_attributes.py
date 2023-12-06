import pandas as pd
import math
import numpy as np
import toml


def merge_attributes(filename_excel, filename_toml_in, filename_toml_out):
    with open(filename_toml_in, "r") as f:
        data_toml = toml.load(f)

    # read by default 1st sheet of an excel file
    data_excel = pd.read_excel('inventory.xlsx')

    column_tags = ["tariff code", "country of origin"]
    all_tags = ["item"] + column_tags

    # prune data
    data_excel = data_excel[all_tags]

    items_xlsx = {}

    for _, row in data_excel.iterrows():
        if row.isnull().values.any():
            continue
        name = row["item"]
        if name in items_xlsx:
            print(f"WARNING: '{name}' duplicate in '{filename_excel}'")
        attributes = {tag: str(row[tag]) for tag in column_tags}
        if len(attributes) == 0:
            print(f"WARNING: no attributes for '{name}' in '{filename_excel}'")
        items_xlsx[name] = {"attributes": attributes}

    items_toml = {}

    for item in data_toml["items"]:
        if "item" not in item or len(item["item"]) == 0:
            continue
        if "item" in items_toml:
            print(f"WARNING: '{item}' duplicate in '{filename_toml_in}'")
        name = item["item"][0]
        items_toml[name] = item

    # all names found
    names_xlsx = set(items_xlsx.keys())
    names_toml = set(items_toml.keys())

    for name in (names_toml - names_xlsx):
        print(f"WARNING: '{name}' not found in '{filename_excel}'")

    for name in (names_xlsx - names_toml):
        print(f"WARNING: '{name}' not found in '{filename_toml_in}'")

    n_updated = 0
    for name in items_toml:
        if name not in items_xlsx:
            continue

        attributes_xlsx = items_xlsx[name]["attributes"]
        attributes_toml = items_toml[name].get("attributes", {})

        if attributes_xlsx == attributes_toml:
            continue

        items_toml[name]["attributes"] = attributes_xlsx

        print(items_toml[name]["attributes"])

        n_updated += 1

    print(f"{n_updated} items updated.")

    # fix-up style
    txt_out = toml.dumps(data_toml)
    txt_out = txt_out.replace("\n[items.attributes]", "[items.attributes]")
    txt_out = txt_out.replace("\n[[items]]", "\n\n[[items]]")
    with open(filename_toml_out, "w") as f:
        f.write(txt_out)


def main():
    merge_attributes("inventory.xlsx",
                     "../public/inv.toml",
                     "../public/inv.toml")


if __name__ == "__main__":
    main()
