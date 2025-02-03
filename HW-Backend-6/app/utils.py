import json 

def parse_cart_string(cart_str: str) -> str:
    inner_str = cart_str.strip('[]')
    dict_strings = inner_str.split('}, {')

    processed_dicts = []
    for dict_str in dict_strings:
        dict_str = dict_str.strip('{}')
        pairs = dict_str.split(',')

        processed_pairs = []
        for pair in pairs:
            key, value = pair.strip().split(':')
            processed_pair = f'"{key.strip()}": "{value.strip()}"'
            processed_pairs.append(processed_pair)

        processed_dict = '{' + ', '.join(processed_pairs) + '}'
        processed_dicts.append(processed_dict)

    result = '[' + ', '.join(processed_dicts) + ']'
    return result



def json_validator(cart: str) -> list[dict]: 
    try:
        cart_json = json.loads(cart)
    except json.JSONDecodeError:
        try:
            proper_json_string = parse_cart_string(cart)
            cart_json = json.loads(proper_json_string)
        except (json.JSONDecodeError, ValueError):
            cart_json = []
    return cart_json


