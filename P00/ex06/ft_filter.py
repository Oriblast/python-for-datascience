def ft_filter(function, iterable):
    """construction of list filter"""
    if function is None:
        return [item for item in iterable if item]
    else:
        return [item for item in iterable if function(item)]
