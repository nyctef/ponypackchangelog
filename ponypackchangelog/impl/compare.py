def compare(old:dict, new:dict) -> dict:
    """
    compare two dictionaries to find entries that are added, removed, and changed

    @type old: dictionary
    @type new: dictionary
    """
    result = {}
    for key in iter(new):
        if key in old:
            if new[key] == old[key]:
                result[key] = "<same>"
            else: 
                result[key] = (old[key], new[key])
        else:
            result[key] = "<added>"

    for key in iter(old):
        if key not in new:
            result[key] = "<removed>"

    return result