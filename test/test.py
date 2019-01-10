#coding=utf-8
def ll(inp):
    temp = ''
    count = 2
    while inp and inp[0] == '{' and count > 0:
        temp += inp[0]
        inp = inp[1:]
        count -= 1
    if temp:
        return temp,inp
def rr(inp):
    temp = ''
    count = 2
    while inp and inp[0] == '}' and count > 0:
        temp += inp[0]
        inp = inp[1:]
        count -= 1
    if temp:
        return temp,inp
def my_lex(inp: str) -> str:
    while inp:
        if inp[0] == "{":
            value = ll(inp)
            if value:
                out,inp = value
                yield out
        elif inp[0] == "}":
            value = rr(inp)
            if value:
                out,inp = value
                yield out
        else:
            out,inp = inp[0],inp[1:]
            yield out
#def my_format(inp: str, *args, **kws) -> str:
def my_format(inp: str) -> str:
    if inp == '':
        raise ValueError("Format template is empty")
    inp = my_lex(inp)
    # print( ">>", inp )
    out = []
    inblock = False
    stack = []
    push = stack.append
    pop = stack.pop
    opush = out.append
    maps = {}
    idx = 0
    temp = ''
    for s in inp:
        if len(s) == 1:
            if s == "{":
                if stack:
                    raise ValueError("Format template can't use '{' or '}'")
                push(s)
                inblock = True
                temp = ''
            elif s == "}":
                if stack:
                    pop(-1)
                    temp = ''.join(i for i in temp if i != ' ')
                    if temp:
                        maps[temp] = ''
                        opush((True,temp))
                        temp = ''
                    else:
                        maps[idx] = ''
                        opush((False,idx))
                        idx += 1

                    inblock = False
                else:
                    raise ValueError("Single '}' in format")
            else:
                if inblock:
                    temp += s
                else:
                    opush( (None,s) )
        else:
            if inblock:
                raise ValueError("Format template can't use '{' or '}', the meaing is '{{' or '}}'")
            else:
                opush( (None,s) )
    if stack:
        raise ValueError("Single '{' in format")
    """
    result = ''
    for flag,obj in out:
        if flag is None:
            result += obj
        elif flag is True:
            result += str(kws[obj])
        elif flag is False:
            result += str(args[obj])
    print(">> ",repr(result) )
    """
    result = []
    rpush = result.append
    for flag,obj in out:
        if flag is None:
            rpush( obj )
        elif flag is True:
            rpush( (obj,) )
        elif flag is False:
            rpush( (obj,) )
    # result = [obj for flag,obj in out if flag is None]
    return result, maps#result, maps
def match(template, target):
    old_template = template
    old_target = target
    result, maps = my_format(template)
    target = list(target)
    stack = []
    cur,result = result[0],result[1:]
    i = 0
    length = len(target)
    while i < length:
        s = target[i]
        print( s, cur, result, stack)
        if s == cur:
            cur,result = result[0],result[1:]
        elif result and s != result [0]:
            stack.append( s )
        elif result and s == result [0]:
            maps[cur[0]] = ''.join(stack)
            stack = []
            cur,result = result[0],result[1:]
            continue
        elif result == [] :
            maps[cur[0]] += s
        i += 1
    if result :
        return None
    return maps
inp = "/{ page }-{id}{}"
# print( my_format(inp,233,**{"say-hi":'say'}) )
print( match(inp, "/hello-abc{id}") )
