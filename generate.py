# importing the os Library
import os
 
train_list = r'main/train/images/'
val_list = r'main/val/images/'
path_list1 = r'train_list.txt'
path_list2 = r'val_list.txt'
test_list = r'main/test/images'
path_list3 = r'test_list.txt'

 
 
def findfiles(path,path_list):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
    for file in file_list:
    	# 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        with open(path_list,'a') as f:
            f.write(cur_path+'\n')
            f.close()
 
if __name__ == '__main__':
    findfiles(train_list,path_list1)
    findfiles(val_list, path_list2)
    findfiles(test_list, path_list3)
