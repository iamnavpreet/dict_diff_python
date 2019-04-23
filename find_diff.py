
def pre_process_dict(to_process_dict):
    _temp_dict = dict()
    for diktkey, diktval in to_process_dict.iteritems():
        if not isinstance(diktval, list):
            _temp_dict.setdefault(diktkey, diktval)
        if isinstance(diktval, list):
            for _dikt in diktval:
                for key in _dikt:
                    _temp_dict.setdefault(diktkey, dict()).setdefault(key, list())
                    if isinstance(_dikt[key], list):
                        _temp_dict[diktkey][key].extend(_dikt[key])
                    else:
                        _temp_dict[diktkey][key].append(_dikt[key])
    return _temp_dict


def find_diff(dict_1, dict_2, mismatch_dict):
    result = list(set(dict_1.keys()).symmetric_difference((set(dict_2.keys()))))
    for key in result:
        if key in dict_1:
            mismatch_dict.setdefault("dict1", dict()).setdefault(key, dict_1.pop(key))
        if key in dict_2:
            mismatch_dict.setdefault("dict2", dict()).setdefault(key, dict_2.pop(key))

    for key in dict_1:
        val_dict1 = dict_1.get(key)
        val_dict2 = dict_2.get(key)

        if not val_dict1 and not val_dict2:
            continue

        if isinstance(val_dict1, str):
            if val_dict1 != val_dict2:
                mismatch_dict.setdefault("dict1", dict()).setdefault(key, dict_1.get(key))
                mismatch_dict.setdefault("dict2", dict()).setdefault(key, dict_2.get(key))

        if isinstance(val_dict1, list) and isinstance(val_dict2, list):
            if all(isinstance(x, str) for x in val_dict1) and all(isinstance(x, str) for x in val_dict2):
                fromdict1 = list(set(val_dict1) - set(val_dict2))
                fromdict2 = list(set(val_dict2) - set(val_dict2))
                if fromdict1:
                    mismatch_dict.setdefault("dict1", dict()).setdefault(key, fromdict1)
                if fromdict2:
                    mismatch_dict.setdefault("dict2", dict()).setdefault(key, fromdict2)

            if all(isinstance(x, dict) for x in val_dict1) and all(isinstance(x, dict) for x in val_dict2):
                _tmp_dict_1 = pre_process_dict({"temp": val_dict1}).get("temp")
                _tmp_dict_2 = pre_process_dict({"temp": val_dict2}).get("temp")

                _mismatch_dict = dict()
                returned_diff = find_diff(_tmp_dict_1, _tmp_dict_2, _mismatch_dict)
                if not returned_diff:
                    continue
                for_dict_1 = returned_diff.get("dict1")
                for_dict_2 = returned_diff.get("dict2")
                if for_dict_1:
                    mismatch_dict.setdefault("dict1", dict()).setdefault(key, for_dict_1)
                if for_dict_2:
                    mismatch_dict.setdefault("dict2", dict()).setdefault(key, for_dict_2)

            if all(isinstance(x, list) for x in val_dict1) and all(isinstance(x, list) for x in val_dict2):
                _tmp_dict_1 = pre_process_dict({"temp": val_dict1}).get("temp")
                _tmp_dict_2 = pre_process_dict({"temp": val_dict2}).get("temp")

                _mismatch_dict = dict()
                returned_diff = find_diff(_tmp_dict_1, _tmp_dict_2, _mismatch_dict)
                if not returned_diff:
                    continue
                for_dict_1 = returned_diff.get("dict1")
                for_dict_2 = returned_diff.get("dict2")
                if for_dict_1:
                    mismatch_dict.setdefault("dict1", dict()).setdefault(key, for_dict_1)
                if for_dict_2:
                    mismatch_dict.setdefault("dict2", dict()).setdefault(key, for_dict_2)

        if isinstance(val_dict1, dict) and isinstance(dict_2.get(key), dict):
            _mismatch_dict = dict()
            returned_diff = find_diff(val_dict1, dict_2.get(key), _mismatch_dict)
            if not returned_diff:
                continue
            for_dict_1 = returned_diff.get("dict1")
            for_dict_2 = returned_diff.get("dict2")
            if for_dict_1:
                mismatch_dict.setdefault("dict1", dict()).setdefault(key, for_dict_1)
            if for_dict_2:
                mismatch_dict.setdefault("dict2", dict()).setdefault(key, for_dict_2)

    return mismatch_dict

