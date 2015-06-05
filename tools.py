"""Some formatting tools."""

def int_or_float(x):
    d = float(x)
    return int(d) if int(d) == d else d  

def deploy_schedule(s, start=2010, ind=8):
    """Creates a formatted deployment schedule from a string."""
    ind = ind * ' '
    dep = list(map(int_or_float, s.split()))
    rtn = ''
    for i in range(0, len(dep), 10):
        data = dep[i:i+10]
        rtn += ind + ', '.join(map(str, data)) + ','
        beg = start + i
        end = beg + len(data) - 1
        rtn += '  # {0} - {1}\n'.format(beg, end)
    return rtn
