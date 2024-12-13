import os
import xml.etree.ElementTree as ET

# 定义一个函数用于从XML文件中提取类别信息
def extract_classes_from_xml(xml_file, all_classes):
    # 解析 XML 文件
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # 遍历 XML 文件中的 object 标签，提取类别信息
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in all_classes:
            all_classes[class_name] = len(all_classes)  # 为新类别分配一个 ID
    return all_classes

def convert_xml_to_yolo(xml_folder, txt_folder, classes_file_path):
    all_classes = {}

    # 获取所有 XML 文件
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]

    # 提取类别信息
    for xml_file in xml_files:
        # 获取图像 ID
        image_id = os.path.splitext(xml_file)[0]
        # 从 XML 文件中提取类别信息并更新 all_classes 字典
        all_classes = extract_classes_from_xml(os.path.join(xml_folder, xml_file), all_classes)

        # 打开并处理每个图像对应的 XML 文件
        with open(os.path.join(txt_folder, f'{image_id}.txt'), 'w') as txt_file:
            tree = ET.parse(os.path.join(xml_folder, xml_file))
            root = tree.getroot()

            # 获取图像的尺寸信息
            size = root.find('size')
            if size is None:
                print(f"警告：{xml_file} 文件缺少 <size> 标签")
                continue

            img_width = float(size.find('width').text) if size.find('width') is not None else 0
            img_height = float(size.find('height').text) if size.find('height') is not None else 0

            # 如果图像的宽度或高度为零，跳过此文件并输出警告
            if img_width == 0 or img_height == 0:
                print(f"警告：{xml_file} 图像尺寸无效，跳过此文件")
                continue

            # 遍历 XML 文件中的所有 object 标签，提取标签、边界框信息，并转为 YOLOv5 格式
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                class_id = all_classes[class_name]  # 获取类别 ID

                bbox = obj.find('bndbox')
                x_min = float(bbox.find('xmin').text)
                y_min = float(bbox.find('ymin').text)
                x_max = float(bbox.find('xmax').text)
                y_max = float(bbox.find('ymax').text)

                # 计算宽度和高度以及中心点坐标
                width = x_max - x_min
                height = y_max - y_min
                x_center = (x_min + x_max) / (2 * img_width)
                y_center = (y_min + y_max) / (2 * img_height)

                # 转换为相对坐标
                width /= img_width
                height /= img_height

                # 写入 YOLOv5 格式的行
                line = f"{class_id} {x_center} {y_center} {width} {height}\n"
                txt_file.write(line)

            print(f"{image_id}.xml 转换完成")

    # 写入所有类别信息到 classes.txt 文件
    with open(classes_file_path, 'w') as classes_file:
        for class_name in sorted(all_classes.keys()):  # 按字典序排序
            classes_file.write(f"{class_name}\n")

    print("转换完成，祝愿您顺利！")

def main():
    # 配置文件路径
    xml_folder = 'lab'
    txt_folder = 'labs'
    classes_file_path = 'labs/classes.txt'

    # 确保文件夹存在
    os.makedirs(txt_folder, exist_ok=True)

    # 开始转换
    convert_xml_to_yolo(xml_folder, txt_folder, classes_file_path)

if __name__ == "__main__":
    main()
