def _parse_line(line:str) -> [(str,str)]:
    if (line.startswith('Name=') | line.startswith('Description=') |
        line.startswith('Icon=') | line.startswith('Author=') |
        line.startswith('[')):
        return []

    arr = line.split()
    
    if len(arr) == 0: return []

    if arr[0] == '!': arr = arr[1:]
    filename = arr[0]
    result = []
    for emote in arr[1:]:
        result.append((emote, filename))

    return result

def from_string(themefile:str) -> dict:
    result = {}

    for line in themefile.split("\n"):
        for entry in _parse_line(line):
            result[entry[0]] = entry[1]

    return result

def from_file(themefilepath:str) -> dict:
    f = open(themefilepath, "r")
    text = f.read()
    f.close()
    return from_string(text)