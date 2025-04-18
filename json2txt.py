import json
import os
from tqdm import tqdm
 
 
def convert_label(json_dir, save_dir, classes):
    json_paths = os.listdir(json_dir)
    classes = classes.split(',')
 
    for json_path in tqdm(json_paths):
 
        path = os.path.join(json_dir, json_path)
        with open(path, 'r') as load_f:
            json_dict = json.load(load_f)
        h, w = json_dict['imageHeight'], json_dict['imageWidth']
 
        # save txt path
        txt_path = os.path.join(save_dir, json_path.replace('json', 'txt'))
        txt_file = open(txt_path, 'w')
 
        for shape_dict in json_dict['shapes']:
            label = shape_dict['label']
            label_index = classes.index(label)
            points = shape_dict['points']
 
            points_nor_list = []
 
            for point in points:
                points_nor_list.append(point[0] / w)
                points_nor_list.append(point[1] / h)
 
            points_nor_list = list(map(lambda x: str(x), points_nor_list))
            points_nor_str = ' '.join(points_nor_list)
 
            label_str = str(label_index) + ' ' + points_nor_str + '\n'
            txt_file.writelines(label_str)
 
 
if __name__ == "__main__":
 
    json_dir = 'labels_json'
    save_dir = 'label'
    classes = 'Background,Open blade disconnect switch,Closed blade disconnect switch,Open tandem disconnect switch,Closed tandem disconnect switch,Breaker,Fuse disconnect switch,Glass disc insulator,Porcelain pin insulator,Muffle,Lightning arrester,Recloser,Power transformer,Current transformer,Potential transformer,Tripolar disconnect switch'
 
    convert_label(json_dir, save_dir, classes)