import os

def fix_labels(txt_dir):
    for txt_file in os.listdir(txt_dir):
        if not txt_file.endswith('.txt'):
            continue
        txt_path = os.path.join(txt_dir, txt_file)
        new_lines = []
        changed = False

        with open(txt_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                new_lines.append(line)
                continue
            cls_id = parts[0]
            coords = list(map(float, parts[1:]))
            fixed_coords = []
            for c in coords:
                if c < 0 or c > 1:
                    changed = True
                fixed_c = min(max(c, 0.0), 1.0)  # Clip到0～1之间
                fixed_coords.append(fixed_c)
            new_line = ' '.join([cls_id] + [f'{c:.6f}' for c in fixed_coords])
            new_lines.append(new_line + '\n')
        
        if changed:
            print(f"✏️ Fixed: {txt_file}")
            with open(txt_path, 'w') as f:
                f.writelines(new_lines)

    print("\n✅ All files have been checked and fixed if needed.")

if __name__ == "__main__":
    txt_dir = r"label"  # 你的txt目录
    fix_labels(txt_dir)
