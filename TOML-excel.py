#!/usr/bin/env python3
from collections import defaultdict
import toml
import xlsxwriter

data = toml.load("public/inv.toml")

purpose_source = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))
for item in data["items"]:
    purpose = item["purpose"][0]
    source = item["source"][0]
    category = item["category"][0]
    purpose_source[purpose][source][category].append(item)

workbook = xlsxwriter.Workbook("public/inv.xlsx")
worksheet = workbook.add_worksheet()

# define cell formats
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

fmt_right_bold = workbook.add_format({'align': 'right',
                                      'bold': True,
                                      'border': 1})

# define columns
column_length = [16, 24, 90, 44, 16]
column_field = ("quantity", "item", "description", "unit price", "extended price")

# start writing
worksheet.merge_range(0, 0, 0, 4, "Fab Lab/Class Inventory", fmt_bold_center)
i = 2
i_total_purpose = []
for purpose in data["purposes"]:
    worksheet.merge_range(i, 0, i, 4, purpose, fmt_bold_center)
    worksheet.set_row(i, 30)

    i += 1
    for j, field in enumerate(column_field):
        worksheet.write(i, j, field, fmt_bold_center)

    i += 1
    i_total_category = []
    for source in data["sources"]:
        category_list = purpose_source[purpose][source].keys()

        if not category_list:
            continue

        worksheet.write(i, 0, source, fmt_bold)
        i += 1

        i_start_category = i
        for category in category_list:
            worksheet.write(i, 1, category, fmt_bold)
            i += 1

            for item in purpose_source[purpose][source][category]:
                worksheet.write_number(i, 0, item["quantity"][0], fmt_left)
                worksheet.write(i, 1, item["item"][0] if item["item"] else "", fmt_left)
                worksheet.write(i, 2, item["description"][0] if item["description"] else "", fmt_left)
                worksheet.write_number(i, 3, item["price"][0], fmt_dollar)
                worksheet.write_formula(i, 4, f'=A{i + 1}*D{i + 1}', fmt_dollar)
                i_total_category.append(i)
                i += 1

        txt_total = f'{source} total'
        worksheet.write(i, 3, txt_total, fmt_right_bold)
        worksheet.write_formula(i, 4, f'=SUM(E{i_start_category + 1}:E{i})', fmt_dollar)
        i += 1

    worksheet.write(i, 3, f'{purpose} total', fmt_right_bold)
    txt_sum = ",".join(f"E{i + 1}" for i in i_total_category)
    worksheet.write_formula(i, 4, f'=SUM({txt_sum})', fmt_dollar)
    i_total_purpose.append(i)
    i += 1

worksheet.write(i, 3, "Inventory total", fmt_right_bold)
txt_sum = ",".join(f"E{i + 1}" for i in i_total_purpose)
worksheet.write_formula(i, 4, f'=SUM({txt_sum})', fmt_dollar)

for j, length in enumerate(column_length):
    worksheet.set_column(j, j, width=length)

workbook.close()
