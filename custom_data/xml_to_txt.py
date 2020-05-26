import pandas as pd
import xml.etree.ElementTree as et
import shutil

xtree = et.parse("annotations.xml")
xroot = xtree.getroot()


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


for node in xroot.iter('image'):
    rows = []
    img_id = node.attrib.get("id")
    name = node.attrib.get("name")
    width = node.attrib.get("width")
    height = node.attrib.get("height")

    root1 = et.Element('root')
    root1 = node

    head_list = list()
    for node2 in root1.iter('box'):
        label = node2.attrib.get("label")
        if label == "head":
            occluded = node2.attrib.get("occluded")
            xtl = node2.attrib.get("xtl")
            ytl = node2.attrib.get("ytl")
            xbr = node2.attrib.get("xbr")
            ybr = node2.attrib.get("ybr")

            x, y, w, h = convert([float(width), float(height)], [float(xtl), float(xbr), float(ytl), float(ybr)])

            attribute_dict = {}

            root2 = et.Element('root')
            root2 = node2
            for node3 in root2.iter('attribute'):
                attribute_dict[str(node3.attrib.get("name"))] = node3.text

            if attribute_dict['mask'] == 'yes' and attribute_dict['has_safety_helmet'] == 'yes':
                rows.append((1, x, y, w, h))
            elif attribute_dict['mask'] == 'yes':
                rows.append((2, x, y, w, h))
            elif attribute_dict['has_safety_helmet'] == 'yes':
                rows.append((3, x, y, w, h))
            else:
                rows.append((0, x, y, w, h))

    with open("./labels/" + str(img_id) + ".txt", "w") as text_file:
        for i in rows:
            j = str(i).replace(',', '')
            text_file.write(j[1:len(j) - 1] + '\n')

    shutil.copyfile("./all_images/" + img_id + ".jpg", "./images/" + img_id + ".jpg")
