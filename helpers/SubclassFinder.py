

def FindSubclassesRec(clss):
    """Recursive function to find all subclasses of a class and return them as a list"""
    subclasses = clss.__subclasses__()
    if len(subclasses) == 0:
        return []
    else:
        results = subclasses
        for subclass in subclasses:
            results.extend(FindSubclassesRec(subclass))
        return results
