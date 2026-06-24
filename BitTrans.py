import json
 
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
    # 2. 加载结构体配置
    struct_cfg = json.loads(struct_json_str)
    fields = struct_cfg["fields"]
    result = {}
    text_lines = [f"【{struct_cfg['struct_name']} 解析结果】"]
 
    for field in fields:
        name = field["name"]
        f_type = field["type"]
        off = field["offset"]
        size = field["length"]
        endian = field.get("endian", "little")
 
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
        text_lines.append(f"{name}: {val}")
 
    return result, "\n".join(text_lines)
 
 
# ==================== 测试运行 ====================
if __name__ == "__main__":
    # 1. 原始十六进制字节
    
    raw_hex = "62 01 23 31 33 35 33 20 31 33 32 39 20 31 33 32 39 01 55 AA 00 04 08 11 06 1A 00 0C 05 00 00 00 00 00 00 00 00 05 00 00 00 00 00 00 E8 03 51 E8 03 00 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 03 03 03 03 03 03 03 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 0B 00 00 00 00 00 00 00 00 00 FF 0F 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    raw_hex.replace ( "" , " " )
    # 2. JSON结构体配置（复制上面的JSON）

    jsonFile = './mcudebug.json'
    with open(jsonFile, 'r') as f:
      struct_json_dict = json.load(f)
    print(struct_json_dict)
    struct_json=json.dumps(struct_json_dict) #json.dumps take a dictionary as input and returns a string as output.
    # 3. 执行解析
    res_dict, res_text = parse_bytes_by_json_struct(raw_hex, struct_json)
 
    # 4. 输出结果
    print(res_text)
    print("\n【JSON格式结果】")
    print(json.dumps(res_dict, ensure_ascii=False, indent=2))
 
