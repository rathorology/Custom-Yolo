import xml.etree.ElementTree as et

xtree = et.parse("annotations.xml")
xroot = xtree.getroot()

with open('test.txt') as f:
    lines = f.read().splitlines()

test_image_id = [i.split('/')[-1].split('.')[0] for i in lines]

for node in xroot.iter('image'):

    rows = []
    img_id = node.attrib.get("id")

    if img_id in test_image_id:
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
                xtl = float(node2.attrib.get("xtl"))
                ytl = float(node2.attrib.get("ytl"))
                xbr = float(node2.attrib.get("xbr"))
                ybr = float(node2.attrib.get("ybr"))
                attribute_dict = {}

                root2 = et.Element('root')
                root2 = node2
                for node3 in root2.iter('attribute'):
                    attribute_dict[str(node3.attrib.get("name"))] = node3.text

                if attribute_dict['mask'] == 'yes' and attribute_dict['has_safety_helmet'] == 'yes':
                    rows.append((1, xtl, ytl, xbr, ybr))
                elif attribute_dict['mask'] == 'yes':
                    rows.append((2, xtl, ytl, xbr, ybr))
                elif attribute_dict['has_safety_helmet'] == 'yes':
                    rows.append((3, xtl, ytl, xbr, ybr))
                else:
                    rows.append((0, xtl, ytl, xbr, ybr))

        with open("./input/ground-truth/" + str(img_id) + ".txt", "w") as text_file:
            for i in rows:
                j = str(i).replace(',', '')
                text_file.write(j[1:len(j) - 1] + '\n')
