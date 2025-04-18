import shutil
import random
import os

# 检查文件夹是否存在
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_image(image_dir, name):
    """
    在 image_dir 中查找 name.jpg 或 name.jpeg，返回完整路径
    如果找不到，返回 None
    """
    jpg_path = os.path.join(image_dir, name + '.jpg')
    jpeg_path = os.path.join(image_dir, name + '.jpeg')
    if os.path.exists(jpg_path):
        return jpg_path
    elif os.path.exists(jpeg_path):
        return jpeg_path
    else:
        return None

def split(image_dir, txt_dir, save_dir):
    # 创建文件夹
    mkdir(save_dir)
    images_dir = os.path.join(save_dir, 'images')
    labels_dir = os.path.join(save_dir, 'labels')

    img_train_path = os.path.join(images_dir, 'train')
    img_test_path = os.path.join(images_dir, 'test')
    img_val_path = os.path.join(images_dir, 'val')

    label_train_path = os.path.join(labels_dir, 'train')
    label_test_path = os.path.join(labels_dir, 'test')
    label_val_path = os.path.join(labels_dir, 'val')

    mkdir(images_dir)
    mkdir(labels_dir)
    mkdir(img_train_path)
    mkdir(img_test_path)
    mkdir(img_val_path)
    mkdir(label_train_path)
    mkdir(label_test_path)
    mkdir(label_val_path)

    # 数据集划分比例
    train_percent = 0.8
    val_percent = 0.1
    test_percent = 0.1

    total_txt = os.listdir(txt_dir)
    num_txt = len(total_txt)
    list_all_txt = range(num_txt)

    num_train = int(num_txt * train_percent)
    num_val = int(num_txt * val_percent)
    num_test = num_txt - num_train - num_val

    train = random.sample(list_all_txt, num_train)
    val_test = [i for i in list_all_txt if i not in train]
    val = random.sample(val_test, num_val)

    print("训练集数目：{}, 验证集数目：{}, 测试集数目：{}".format(len(train), len(val), len(val_test) - len(val)))

    for i in list_all_txt:
        name = total_txt[i][:-4]  # 去掉 .txt 后缀

        srcImage = find_image(image_dir, name)
        srcLabel = os.path.join(txt_dir, name + '.txt')

        if srcImage is None:
            print(f"⚠️ Warning: 图片 {name}.jpg / {name}.jpeg 不存在，跳过。")
            continue

        if not os.path.exists(srcLabel):
            print(f"⚠️ Warning: 标注 {name}.txt 不存在，跳过。")
            continue

        if i in train:
            dst_train_Image = os.path.join(img_train_path, os.path.basename(srcImage))
            dst_train_Label = os.path.join(label_train_path, name + '.txt')
            shutil.copyfile(srcImage, dst_train_Image)
            shutil.copyfile(srcLabel, dst_train_Label)
        elif i in val:
            dst_val_Image = os.path.join(img_val_path, os.path.basename(srcImage))
            dst_val_Label = os.path.join(label_val_path, name + '.txt')
            shutil.copyfile(srcImage, dst_val_Image)
            shutil.copyfile(srcLabel, dst_val_Label)
        else:
            dst_test_Image = os.path.join(img_test_path, os.path.basename(srcImage))
            dst_test_Label = os.path.join(label_test_path, name + '.txt')
            shutil.copyfile(srcImage, dst_test_Image)
            shutil.copyfile(srcLabel, dst_test_Label)

if __name__ == '__main__':
    image_dir = 'images'
    txt_dir = 'label'
    save_dir = 'data'

    split(image_dir, txt_dir, save_dir)
    print("数据集划分完成！")
