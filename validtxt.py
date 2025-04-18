import os

def check_labels(txt_dir):
    errors = []
    for txt_file in os.listdir(txt_dir):
        if not txt_file.endswith('.txt'):
            continue
        txt_path = os.path.join(txt_dir, txt_file)
        with open(txt_path, 'r') as f:
            lines = f.readlines()
        
        for idx, line in enumerate(lines):
            parts = line.strip().split()
            # 如果行为空或者只有类别也跳过
            if len(parts) < 5:
                print(f"⚠️ Warning: {txt_file} line {idx+1} has less than 5 elements.")
                continue

            # 第一个是类别id，不检查，后面是x_center, y_center, width, height
            numbers = list(map(float, parts[1:]))
            for num in numbers:
                if num < 0 or num > 1:
                    errors.append((txt_file, idx + 1, num))
    
    if errors:
        print("\n❌ Found errors in the following files:")
        for error in errors:
            print(f"File: {error[0]}, Line: {error[1]}, Value: {error[2]}")
    else:
        print("\n✅ All labels are normalized correctly!")

if __name__ == "__main__":
    txt_dir = r"label"  # 你自己的txt目录
    check_labels(txt_dir)
