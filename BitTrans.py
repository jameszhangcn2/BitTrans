import json
import tkinter as tk
from tkinter import ttk
def bytes_to_bitlist(data: bytes) -> list[int]:
    """字节数组转平坦比特列表，bit0在前"""
    bits = []
    for b in data:
        for i in range(8):
            bits.append((b >> i) & 1)
    return bits
 
def bitlist_to_int(bit_slice: list[int], bit_order: str, signed: bool) -> int:
    """比特切片转整数
    bit_slice: [0,1,0...] 低位在前原始比特
    bit_order: msb_first / lsb_first
    signed: 是否有符号整数
    """
    if bit_order == "msb_first":
        # 比特切片内高位在前，反转顺序计算
        bits = bit_slice[::-1]
    else:
        bits = bit_slice
    val = 0
    for b in bits:
        val = (val << 1) | b
    # 符号位处理
    bit_cnt = len(bit_slice)
    if signed and bits[0] == 1:
        mask = (1 << bit_cnt) - 1
        val = val - (1 << bit_cnt)
    return val

def parse_bytes_by_json_struct(hex_data: str, struct_json_str: str):
    """
    根据JSON定义的结构体解析十六进制字节
    :param hex_data: 空格分隔的十六进制字节串
    :param struct_json_str: 结构体JSON字符串
    :return: 解析结果字典 + 格式化可读文本
    """
    # 1. 十六进制转字节数组
    hex_clean = hex_data.replace(" ", "")
    byte_data = bytes.fromhex(hex_clean)
    full_bitlist = bytes_to_bitlist(byte_data)
    # 2. 加载结构体配置
    struct_cfg = json.loads(struct_json_str)
    fields = struct_cfg["fields"]
    result = {}
    text_lines = [f"【{struct_cfg['struct_name']} 解析结果】"]
 
    for field in fields:
        name = field["name"]
        f_type = field["type"]
        
        endian = field.get("endian", "little")
        bit_order = field.get("bit_order", "msb_first")
        use_bit_mode = "bit_offset" in field

        # 分支1：比特粒度解析（仅整数）
        if use_bit_mode:
            if f_type in ("ascii", "hex"):
                raise ValueError(f"字段 {name}: ascii/hex 不支持比特模式，只能使用offset/length字节模式")
            bit_off = field["bit_offset"]
            bit_len = field["bit_length"]
            # 边界校验
            if bit_off + bit_len > len(full_bitlist):
                raise ValueError(f"字段 {name} 比特超出数据流范围：总比特{len(full_bitlist)}, 结束位置{bit_off+bit_len}")
            # 截取比特段
            bit_seg = full_bitlist[bit_off : bit_off + bit_len]
            # 判断是否有符号
            signed = f_type.startswith("i")
            val = bitlist_to_int(bit_seg, bit_order, signed)
            # 多字节比特段端序处理（比特总长度≥8bit）
            total_byte = bit_len // 8
            if total_byte >= 1 and bit_len % 8 == 0:
                raw_bytes = val.to_bytes(total_byte, byteorder="big", signed=signed)
                val = int.from_bytes(raw_bytes, byteorder=endian, signed=signed)
 
        # 分支2：原有字节粒度解析（兼容旧逻辑）
        else:
            off = field["offset"]
            size = field["length"]
            # 截取对应字节段
            seg = byte_data[off: off + size]
            val = None
    
            # 按类型解码
            if f_type == "ascii":
                # ASCII字符串，截断空字符
                val = seg.decode("ascii", errors="replace").split("\x00")[0]
            elif f_type == "u8":
                val = int.from_bytes(seg, byteorder="big", signed=False)
            elif f_type == "i8":
                val = int.from_bytes(seg, byteorder="big", signed=True)
            elif f_type in ("u16", "u32"):
                val = int.from_bytes(seg, byteorder=endian, signed=False)
            elif f_type in ("i16", "i32"):
                val = int.from_bytes(seg, byteorder=endian, signed=True)
            elif f_type == "hex":
                val = seg.hex(" ")
 
        result[name] = val
        if use_bit_mode:
            text_lines.append(f"{name} [bit{field['bit_offset']}~bit{field['bit_offset']+field['bit_length']-1}]: {val}")
        else:
            text_lines.append(f"{name} [byte{field['offset']}~byte{field['offset']+field['length']-1}]: {val}")
 
    return result, "\n".join(text_lines)
 
 
def show_result():
    # 获取两个多行文本框内容
    jsonFile = input_text1.get(1.0, tk.END).strip()
    with open(jsonFile, 'r') as f:
      struct_json_dict = json.load(f)
    print(struct_json_dict)
    struct_json=json.dumps(struct_json_dict) #json.dumps take a dictionary as input and returns a string as output.

    raw_hex = input_text2.get(1.0, tk.END).strip()
    raw_hex.replace ( "" , " " )

    # 3. 执行解析
    res_dict, res_text = parse_bytes_by_json_struct(raw_hex, struct_json)

    # 4. 输出结果
    print(res_text)
    print("\n【JSON格式结果】")
    print(json.dumps(res_dict, ensure_ascii=False, indent=2))

    # 解析结果并写入输出框
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, json.dumps(res_dict, ensure_ascii=False, indent=2))

# 创建主窗口
root = tk.Tk()
root.title("Bytes Trans")
root.geometry("650x520")
 
# 第一组：输入框1 + 滚动条
frame1 = tk.Frame(root)
frame1.pack(pady=2)
tk.Label(frame1, text="json file:").pack(anchor="w")
text_frame1 = tk.Frame(frame1)
text_frame1.pack()
input_text1 = tk.Text(text_frame1, width=65, height=1)
scroll1 = tk.Scrollbar(text_frame1, command=input_text1.yview)
input_text1.configure(yscrollcommand=scroll1.set)
input_text1.grid(row=0, column=0)
scroll1.grid(row=0, column=1, sticky="ns")
#set default  text
default_text="./mcudebug.json"
input_text1.insert(1.0,default_text)
 
# 第二组：输入框2 + 滚动条
frame2 = tk.Frame(root)
frame2.pack(pady=2)
tk.Label(frame2, text="Bytes:").pack(anchor="w")
text_frame2 = tk.Frame(frame2)
text_frame2.pack()
input_text2 = tk.Text(text_frame2, width=65, height=5)
scroll2 = tk.Scrollbar(text_frame2, command=input_text2.yview)
input_text2.configure(yscrollcommand=scroll2.set)
input_text2.grid(row=0, column=0)
scroll2.grid(row=0, column=1, sticky="ns")
 
# 按钮
tk.Button(root, text="Translate", command=show_result).pack(pady=6)
 
# 第三组：输出框 + 滚动条
frame3 = tk.Frame(root)
frame3.pack(pady=2)
tk.Label(frame3, text="Result").pack(anchor="w")
text_frame3 = tk.Frame(frame3)
text_frame3.pack()
output_text = tk.Text(text_frame3, width=80, height=15)
scroll3 = tk.Scrollbar(text_frame3, command=output_text.yview)
output_text.configure(yscrollcommand=scroll3.set)
output_text.grid(row=0, column=0)
scroll3.grid(row=0, column=1, sticky="ns")
 
root.mainloop()

 
