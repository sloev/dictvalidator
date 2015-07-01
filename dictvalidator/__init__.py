# Maps of string key to function

_tmp = "__temp__"
def validate_dict(full_expression, data):
    if not _tmp in full_expression:
        full_expression[_tmp] = {}
    def _eq(a,b):
        return a==b
    def _gt(a,b):
        return a>b
    def _gte(a,b):
        return a>=b
    def _lt(a,b):
        return a<b
    def _lte(a,b):
        return a<=b
    def _neq(a,b):
        return not a==b
    def _contains(a,b):
        return a in b
    def _icontains(a,b):
        '''
        supports X in ["lol", 10, "cat]
        and
        X in "lolcat"
        '''
        try:
            _b = full_expression[_tmp]['icontains']
        except KeyError:
            if isinstance(b, list):
                _b = [x.lower() if isinstance(x, str) else x for x in b]
            elif isinstance(b,str):
                _b = b.lower()
            full_expression[_tmp]["icontains"] = _b
        if isinstance(a, str):
            return a.lower() in _b
        return a in _b

    def _startswith(a,b):
        if isinstance(a, str):
            return a.startswith(b)

    def _istartswith(a,b):
        try:
            _b = full_expression[_tmp]['istartswith']
        except KeyError:
            if isinstance(b, str):
                _b = b.lower()
            else:
                _b = b
            full_expression[_tmp]['istartswith'] = _b
        if isinstance(a, str):
            return a.lower().startswith(_b)
    def _endswith(a,b):
        if isinstance(a, str):
            return a.endswith(b)
    def _iendswith(a,b):
        try:
            _b = full_expression[_tmp]['iendswith']
        except KeyError:
            if isinstance(b, str):
                _b = b.lower()
            else:
                _b = b
            full_expression[_tmp]['iendswith'] = _b
        if isinstance(a, str):
            return a.endswith(_b)

    _operator_map = {
            "eq":           _eq,
            "gt":           _gt,
            "gte":          _gte,
            "lt":           _lt,
            "lte":          _lte,
            "neq":          _neq,
            "contains":     _contains,
            "icontains":    _icontains,
            "startswith":   _startswith,
            "istartswith":  _istartswith,
            "endswith":     _endswith,
            "iendswith":    _iendswith
            }
    def validate(expression):
        operator = expression.keys()[0]
        if operator.startswith("_"):
            print "fuck"
        elif operator == "all":
            res = True
            for sub_expression in expression[operator]:
                res = res and validate(sub_expression)
            return res
        elif operator == "any":
            res = False
            for sub_expression in expression[operator]:
                res = res or validate(sub_expression)
            return res
        else:
            a = expression[operator][0]
            b = data[a]
            c = expression[operator][1]
            try:
                res =  _operator_map[operator](b,c)
                if not res:
                    raise TypeError
                return True
            except TypeError,e:
                print "[validator fail:",type(b),b," [", operator,"]",type(c),c,"]:"
                return False
    res = validate(full_expression)
    #print "RES:%s\n"%str(res)
    return res

