#!/usr/bin/env python3
from collections import defaultdict
import toml
import xlsxwriter

#
# read TOML
#
data = toml.load("public/inv.toml")

attributes = []

#
# build tree
#
item_tree = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))
attributes_found = set()
for item in data["items"]:
    purpose = item["purpose"][0]
    source = item["source"][0]
    category = item["category"][0]
    # sanitize
    if not item["item"]:
        item["item"] = [""]
    if not item["description"]:
        item["description"] = [""]
    if "attributes" not in item:
        item["attributes"] = {}
    item_tree[purpose][source][category].append(item)
    attributes_found |= item["attributes"].keys()
attributes = sorted(attributes_found)

#
# create sheet
#
workbook = xlsxwriter.Workbook("public/inv.xlsx")
worksheet = workbook.add_worksheet()

#
# cell formats
#
fmt_bold = workbook.add_format({"bold": True,
                                'border': 1})

fmt_bold_center = workbook.add_format({"bold": True,
                                       'border': 1})
fmt_bold_center.set_align('center')
fmt_bold_center.set_align('vcenter')

fmt_dollar = workbook.add_format({'num_format': '$#,##0.00',
                                  'align': 'right',
                                  'border': 1})

fmt_left = workbook.add_format({'align': 'left',
                                'border': 1})

fmt_link = workbook.add_format({'align': 'left',
                                'underline': True,
                                'border': 1})

fmt_link_center = workbook.add_format({'underline': True,
                                       'bold': True,
                                       'border': 1})
fmt_link_center.set_align('center')
fmt_link_center.set_align('vcenter')

fmt_right_bold = workbook.add_format({'align': 'right',
                                      'bold': True,
                                      'border': 1})

# set column size
column_length = [16, 24, 100, 46, 16]
column_field = ["quantity", "item", "description", "unit price", "extended price"]
for a in attributes:
    column_length.append(16)
    column_field.append(a)
for j, length in enumerate(column_length):
    worksheet.set_column(j, j, width=length)

# write title
worksheet.merge_range(0, 0, 0, 4, "", fmt_link_center)
worksheet.write_url(0, 0, "http://inventory.fabcloud.io/",
                    string="Fab Lab/Class Inventory",
                    cell_format=fmt_link_center)

i = 2
i_total_purpose = []
for purpose, purpose_info in data["purposes"].items():
    worksheet.merge_range(i, 0, i, 4, purpose, fmt_link_center)

    # write purpose
    if purpose_info["URL"]:
        worksheet.write_url(i, 0, purpose_info["URL"][0], string=purpose, cell_format=fmt_link_center)
    else:
        worksheet.write(i, 0, purpose, fmt_link_center)
    worksheet.set_row(i, 30)  # increase cell height, in pt
    i += 1

    # write field names
    for j, field in enumerate(column_field):
        worksheet.write(i, j, field, fmt_bold_center)
    i += 1

    i_total_category = []
    for source, source_info in data["sources"].items():
        category_list = item_tree[purpose][source].keys()

        if not category_list:
            continue

        # write source
        if source_info["URL"]:
            worksheet.write_url(i, 0, source_info["URL"][0], string=source, cell_format=fmt_link_center)
        else:
            worksheet.write(i, 0, source, fmt_bold)
        i += 1

        i_start_category = i
        for category in category_list:
            # write category
            worksheet.write(i, 1, category, fmt_bold)
            i += 1

            for item in item_tree[purpose][source][category]:
                # write item
                worksheet.write_number(i, 0, item["quantity"][0], fmt_left)
                if item["URL"]:
                    worksheet.write_url(i, 1, item["URL"][0], string=item["item"][0], cell_format=fmt_link)
                else:
                    worksheet.write(i, 1, item["item"][0], fmt_left)
                worksheet.write(i, 2, item["description"][0], fmt_left)
                worksheet.write_number(i, 3, item["price"][0], fmt_dollar)
                worksheet.write_formula(i, 4, f'=A{i + 1}*D{i + 1}', fmt_dollar)
                for k, a in enumerate(attributes):
                    if a in item["attributes"]:
                        worksheet.write(i, 5+k, item["attributes"][a], fmt_left)
                i_total_category.append(i)
                i += 1

        # write source total
        worksheet.write(i, 3, f'{source} total', fmt_right_bold)
        worksheet.write_formula(i, 4, f'=SUM(E{i_start_category + 1}:E{i})', fmt_dollar)
        i += 1

    # write purpose total
    worksheet.write(i, 3, f'{purpose} total', fmt_right_bold)
    txt_sum = ",".join(f"E{i + 1}" for i in i_total_category)
    worksheet.write_formula(i, 4, f'=SUM({txt_sum})', fmt_dollar)
    i_total_purpose.append(i)
    i += 1

# write inventory total
worksheet.write(i, 3, "Inventory total", fmt_right_bold)
txt_sum = ",".join(f"E{i + 1}" for i in i_total_purpose)
worksheet.write_formula(i, 4, f'=SUM({txt_sum})', fmt_dollar)

workbook.close()
