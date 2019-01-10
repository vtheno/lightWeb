import re
def build_route_regexp(string):
    def named_groups(obj):
        return '(?P<{obj}>[a-zA-Z0-9_-]+)'.format(obj=obj.group(1))
    re_string = re.sub(r'{([a-zA-Z0-9_-]+)}', named_groups, string)
    re_string = '^' + re_string + '$'
    return re.compile(re_string) 
pattern = build_route_regexp('/{hello}')
print( pattern, dir(pattern) )
value = pattern.match('/vtheno')
print( value.groupdict() )
