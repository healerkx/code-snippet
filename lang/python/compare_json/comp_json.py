
import json


def make_key(parent_key, key):
    return f"{parent_key}.{key}" if len(parent_key) > 0 else key

def is_equal_items(va, vb, ignore_fileds, parent_key):
    if type(va) != type(vb):
        return False
    if isinstance(va, str) or isinstance(va, int) or isinstance(va, float) or isinstance(va, bool):
        if va != vb: return False
    elif isinstance(va, list):
        if not comp_json_array(va, vb, ignore_fileds, parent_key): return False
    else:
        if not comp_json_obj(va, vb, ignore_fileds, parent_key): return False
    return True

def comp_json_array(a, b, ignore_fileds, parent_key):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        va, vb = a[i], b[i]
        full_key = make_key(parent_key, str(i))
        if not is_equal_items(va, vb, ignore_fileds, full_key):
            return False
    return True


def comp_json_obj(a, b, ignore_fileds, parent_key):
    # TODO: a 直接是个数组
    keys = [key for key in a.keys()]
    keys += [key for key in b.keys()]
    for key in set(keys):
        full_key = make_key(parent_key, key)

        if full_key in ignore_fileds:
            continue

        if (key in a) != (key in b):
            return False
        va, vb = a[key], b[key]
        if not is_equal_items(va, vb, ignore_fileds, full_key):
            return False
    
    return True


def comp_json(a, b, ignore_fileds):
    return comp_json_obj(json.loads(a), json.loads(b), ignore_fileds, '')

# 完全相等的情况
a1 = json.dumps({"a":1, "b": {"c": 1.1, "d": [1, 2]}, "d": "d"})
a2 = json.dumps({"a":1, "b": {"c": 1.1, "d": [1, 2]}, "d": "d"}) 
print(comp_json(a1, a2, []))

# 类型不一致
a1 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2]}})
a2 = json.dumps({"a":1, "b": {"c": 1, "d": [1, 2]}})
print(comp_json(a1, a2, []))

# 2级数组数量不一致
a1 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2]}})
a2 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2, 3]}})
print(comp_json(a1, a2, []))

# 2级数组内容不一致
a1 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2]}})
a2 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2.0]}})
print(comp_json(a1, a2, []))

# 2级数组内容不一致, 但是忽略了
a1 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2]}})
a2 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2.0]}})
print(comp_json(a1, a2, ["b.d"]))

# 空数组比较
a1 = json.dumps({})
a2 = json.dumps({})
print(comp_json(a1, a2, []))

# b.c的内容不一致
a1 = json.dumps({"a":1, "b": {"c": 1.0, "d": [1, 2]}})
a2 = json.dumps({"a":1, "b": {"c": 1, "d": [1, 2]}})
print(comp_json(a1, a2, ["b.d"]))