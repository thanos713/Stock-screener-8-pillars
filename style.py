def percentage(x, pos):
    'The two args are the value and tick position'
    return '%1.1f' % (x * 1)

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)

def billions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fB' % (x * 1e-9)

def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.1fK' % (x * 1e-3)

def num_to_string(x):
    if x >= 1e12:
        return '%1.1fT' % (x * 1e-12)
    elif x>= 1e9:
        return '%1.1fB' % (x * 1e-9)
    elif x>=1e6:
        return '%1.1fM' % (x * 1e-6)
    else:
        return '%1.1fK' % (x * 1e-3)

    
def string_to_num(x):
    if "T" in x:
        x = x.replace('T','')
        x = float(x)*1e12
    elif "B" in x:
        x = x.replace('B','')
        x = float(x)*1e9
    elif "M" in x:
        x = x.replace('M','')
        x = float(x)*1e6
    elif "Κ" in x:
        x = x.replace('K','')
        x = float(x)*1e3
    return x
    
def f(x):
    return '{0:.3g}'.format(x)