from collections import defaultdict

def flot_values(queryset=None):
    """
    Takes a queryset and iterates over them to create a list of values for use
    in a jQuery flot chart
    """
    if queryset:
        d = defaultdict(int)
        for i in queryset:
            d[i.created_at.strftime("%Y%m%d")] += 1
        return [v for k,v in d.iteritems()]
    else:
        return None 