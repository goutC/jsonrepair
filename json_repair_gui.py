import json
from tkinter import (
    filedialog, messagebox, scrolledtext,
    Tk, Button, END, Label, Spinbox
)
from collections import OrderedDict

# 默认最大递归深度
DEFAULT_DEPTH = 5

def remove_duplicate_keys_limited_depth(json_text, max_depth):
    def process_pairs(pairs, depth=0):
        result = OrderedDict()
        for key, value in pairs:
            if key not in result:
                if isinstance(value, list) and depth < max_depth:
                    value = [handle_nested(v, depth + 1) for v in value]
                elif isinstance(value, dict) and depth < max_depth:
                    value = process_pairs(value.items(), depth + 1)
                result[key] = value
        return result

    def handle_nested(obj, depth):
        if isinstance(obj, dict):
            return process_pairs(obj.items(), depth)
        elif isinstance(obj, list):
            return [handle_nested(item, depth) for item in obj]
        else:
            return obj

    return json.loads(json_text, object_pairs_hook=lambda pairs: process_pairs(pairs, 0))

# 主操作函数
def open_and_repair_json():
    filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not filepath:
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = f.read()

        max_depth = int(depth_spinbox.get())
        repaired_data = remove_duplicate_keys_limited_depth(json_data, max_depth)
        pretty = json.dumps(repaired_data, indent=2, ensure_ascii=False)

        output_text.delete(1.0, END)
        output_text.insert(END, pretty)

        messagebox.showinfo("修复成功", "JSON 修复成功，重复键已移除。")

    except Exception as e:
        messagebox.showerror("错误", f"处理失败：\n{e}")

# 保存结果
def save_repaired_json():
    data = output_text.get(1.0, END).strip()
    if not data:
        messagebox.showwarning("提示", "没有可以保存的内容")
        return

    filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not filepath:
        return

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data)
        messagebox.showinfo("保存成功", f"文件已保存：\n{filepath}")
    except Exception as e:
        messagebox.showerror("保存失败", str(e))


# GUI 构建
root = Tk()
root.title("JSON 修复工具（去重键 + 深度控制）")

# 控件布局
btn_open = Button(root, text="打开并修复 JSON", command=open_and_repair_json)
btn_open.pack(pady=5)

depth_label = Label(root, text="递归深度（2-10）：")
depth_label.pack()

depth_spinbox = Spinbox(root, from_=2, to=10, width=5)
depth_spinbox.pack()
depth_spinbox.delete(0, END)
depth_spinbox.insert(0, DEFAULT_DEPTH)

output_text = scrolledtext.ScrolledText(root, width=100, height=30)
output_text.pack(padx=10, pady=10)

btn_save = Button(root, text="另存为", command=save_repaired_json)
btn_save.pack(pady=5)

root.mainloop()
