
def find_depth(data, depth=0):
    result = []
    
    # If data is a dictionary, iterate through its keys
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'data':
                pass
            else:    
                result.append((key, depth))  # Add key and current depth to result
                result.extend(find_depth(value, depth + 1))  # Recurse into the value with increased depth
    
    # If data is a list, iterate through its elements
    elif isinstance(data, list):
        for item in data:
            result.extend(find_depth(item, depth + 1))  # Recurse into list item with increased depth
    
    return result
    

def find_key(data, target_key, path=None):
    """
    Recursively search for a key in multi-layer JSON data.

    :param data: The JSON data (can be a dict, list, etc.)
    :param target_key: The key to search for
    :param path: Internal parameter to keep track of the current path
    :return: A list of tuples containing the key path and value
    """
    if path is None:
        path = []

    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append((path + [key], value))
            results.extend(find_key(value, target_key, path + [key]))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            results.extend(find_key(item, target_key, path + [f"[{index}]"]))

    return results

def find_key_value(data, target_key):
    """
    Recursively searches for a key-value pair in a nested JSON structure.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, (dict, list)):
                result = find_key_value(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_value(item, target_key)
            if result is not None:
                return result
    return None

def RemoveChildToParent(Dic):
    try:
        SectionKey = []
        for m in Dic:
            for key, value in m.items():
                SectionKey.append(key)

        for sk in range(len(SectionKey)):   
            removeChildToParent = ''            
            for m in Dic:
                for key, value in m.items():
                    if value['child'] == SectionKey[sk]:
                        removeChildToParent = value['child']
                        
            for m in Dic:
                for key, value in m.items():
                    if key == removeChildToParent:
                        Dic.remove(m)
                        break          
        return Dic            
    except Exception as error:
        print("error", error)  

def DuplicateKeyUniqueItem(Dic):
    try:
        ItemUnique = []
        keyUniqueItem = []
        for m in Dic:
            for key, value in m.items():
                keyUniqueItem.append(key)

        count = 0
        for kui in list(set(keyUniqueItem)):
            for m in Dic:
                for key, value in m.items():
                    if kui == key:
                        count+=1
                        if count<=len(list(set(keyUniqueItem))):
                            ItemUnique.append(m)
                       
        return ItemUnique               
    except Exception as error:
        print("error", error)    



def DynamicFlowchart(data):
    try:
        processType = ''
        Dic = {
            'fl1':[],
            'fl2':[],
            'fl3':[],
            'fl4':[],
            'fl5':[],
        }

        for d in data:
            if d != 'merge_data':
                processType = data[d]['data']['data']['container']['processType']
                depth = find_depth(data[d])
                for dph in depth:
                    if dph[1] == 0:
                        result1 = find_key_value(data, dph[0])
                        count = 0
                        for r in result1:
                            if r == 'data':
                                count +=1
                                if count == 1:
                                    Dic['fl1'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": 'null',
                                        }    
                                    })
                            else:
                                count +=1
                                if count == 1:
                                    Dic['fl1'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": r,
                                        }    
                                    })

                    elif dph[1] == 1:
                        result1 = find_key_value(data, dph[0])
                        count = 0
                        for r in result1:
                            if r == 'data':
                                count +=1
                                if count == 1:
                                    Dic['fl2'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": 'null',
                                        }    
                                    })
                            else:
                                count +=1
                                if count == 1:
                                    Dic['fl2'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": r,
                                        }    
                                    })
        
                    elif dph[1] == 2:
                        result1 = find_key_value(data, dph[0])
                        count = 0
                        for r in result1:
                            if r == 'data':
                                count +=1
                                if count == 1:
                                    Dic['fl3'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": 'null',
                                        }    
                                    })
                            else:
                                count +=1
                                if count == 1:
                                    Dic['fl3'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": r,
                                        }    
                                    })


                    elif dph[1] == 3:
                        result1 = find_key_value(data, dph[0])
                        count = 0
                        for r in result1:
                            if r == 'data':
                                count +=1
                                if count == 1:
                                    Dic['fl4'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": 'null',
                                        }    
                                    })
                            else:
                                count +=1
                                if count == 1:
                                    Dic['fl4'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": r,
                                        }    
                                    })

                    elif dph[1] == 4:
                        result1 = find_key_value(data, dph[0])
                        count = 0
                        for r in result1:
                            if r == 'data':
                                count +=1
                                if count == 1:
                                    Dic['fl5'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": 'null',
                                        }    
                                    })
                            else:
                                count +=1
                                if count == 1:
                                    Dic['fl5'].append({dph[0]: {
                                            "type": result1['data']['type'],
                                            "data": result1['data']['data'],
                                            "child": r,
                                        }    
                                    })

                Dic['fl2'] = RemoveChildToParent(Dic['fl2'])
                Dic['fl2'] = DuplicateKeyUniqueItem(Dic['fl2'])
                Dic['fl3'] = RemoveChildToParent(Dic['fl3'])
                Dic['fl3'] = DuplicateKeyUniqueItem(Dic['fl3'])
                Dic['fl4'] = RemoveChildToParent(Dic['fl4'])
                Dic['fl4'] = DuplicateKeyUniqueItem(Dic['fl4'])
                Dic['fl5'] = RemoveChildToParent(Dic['fl5'])
                Dic['fl5'] = DuplicateKeyUniqueItem(Dic['fl5'])
                # print("Dic", Dic)    
        return processType, Dic
    except Exception as error:
        print("254 error", error)
