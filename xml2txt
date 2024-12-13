# 实现xml格式转yolov5格式

import os
import xml.etree.ElementTree as ET

# 定义一个函数用于从XML文件中提取类别信息
def extract_classes_from_xml(xml_file, all_classes):
    global tree
    tree = ET.parse(xml_file)
    for obj in tree.findall('object'):
        class_name = obj.find('name').text
        if class_name not in all_classes:
            all_classes[class_name] = len(all_classes)
    return all_classes

def main():
    # 准备保存 classes 信息的文件
    classes_file_path = 'lab/classes.txt'

    # 遍历XML文件夹
    xml_folder = 'lab'
    txt_folder = 'labs'

    all_classes = {}

    # 准备保存类别信息的文件
    with open(classes_file_path, 'w') as classes_file:
        for xml_file in os.listdir(xml_folder):
            if not xml_file.endswith('.xml'):
                continue

            image_id = os.path.splitext(xml_file)[0]

            # 从XML文件中提取类别信息
            all_classes = extract_classes_from_xml(os.path.join(xml_folder, xml_file), all_classes)

            with open(os.path.join(txt_folder, f'{image_id}.txt'), 'w') as txt_file:
                for obj in ET.parse(os.path.join(xml_folder, xml_file)).findall('object'):
                    class_name = obj.find('name').text
                    class_id = all_classes[class_name]

                    bbox = obj.find('bndbox')
                    x_min = float(bbox.find('xmin').text)
                    y_min = float(bbox.find('ymin').text)
                    x_max = float(bbox.find('xmax').text)
                    y_max = float(bbox.find('ymax').text)

                    width = x_max - x_min
                    height = y_max - y_min
                    x_center = x_min + width / 2
                    y_center = y_min + height / 2

                    img_width = float(tree.find('size').find('width').text)
                    img_height = float(tree.find('size').find('height').text)

                    x_center /= img_width
                    y_center /= img_height
                    width /= img_width
                    height /= img_height

                    line = f"{class_id} {x_center} {y_center} {width} {height}\n"
                    txt_file.write(line)

            print(f" {image_id}.xml to {image_id}.txt 转换完成")

        for class_name, class_id in all_classes.items():
            classes_file.write(f"{class_name}\n")

    print("转换完成，祝愿您顺利")

if __name__ == "__main__":
    main()
