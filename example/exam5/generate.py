#coding=utf-8
class Data(object):
    def __init__(self,col:int,row:int,color:str,content:str):
        self.col = col
        self.row = row
        self.color = color
        self.content = content
    def __repr__(self):
        return f"""{{ col: 'col{self.col}', row: 'row{self.row}', color: {self.color!r}, content: {self.content!r} }}"""

def vueJS(datas:[Data]):
    return f"""
var app = new Vue({{
    el: '#app',
    data: {{
        poss: {datas}
    }}
}})
"""

# display grid 拥有如下属性
# grid-template-columns 设置几列显示就几个值 具体值 和 百分比
# grid-template-rows
# grid-row 是 grid-row-start 和 grid-row-end 的缩写
# grid-column,grid-row 指定 1 值 表示 row-start | column-start
#                      指定 2 值 表示 row-end | column-start
# grid-area 是 grid-row-start,grid-column-start,grid-row-end,grid-column-end
# span 用来跨越 行 或 列 的数量 可以手动计算 start 和 end

def grid(col,row):
    return f"""
body {{
    width: 100%;
    scroll: auto;
}}
.grid {{
    display: grid;
    width: 100%;
    height: 100%;
    color: #FFF;
    /* grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr; */
    grid-template-columns: repeat({col},1fr);
    grid-template-rows: repeat({row},1fr);
    grid-gap: 5px;
    position: absolute;
    left: 0%;
    top: 0%;
}}
.col_all {{
    grid-column-start: 1;
    grid-column-end: {col+1};
}}
"""
def colorTheme():
    return """
.lightblue{
    background-color: lightblue;
}
.lightsalmon{
    background: lightsalmon;
}
.lightpink{
    background: lightpink;
}
.lightskyblue{
    background: lightskyblue;
}
"""
def row_span(i,n):
    return f"""
.row_{i}_{n} {{
    grid-row-start: {i};
    grid-row-end: {i+n};
}}
"""
def col_span(i,n):
    return f"""
.col_{i}_{n} {{
    grid-column-start: {i};
    grid-column-end: {i+n};
}}
"""
def row_index(i):
    return f"""
.row{i} {{
    grid-row-start: {i};
    grid-row-end: {i};
}}
"""
def col_index(i):
    return f"""
.col{i} {{
    grid-column-start: {i};
    grid-column-end: {i};
}}
"""

def grid_style(col,row):
    result = colorTheme()
    result += grid(col,row)
    result += ''.join(col_index(i) for i in range(1,col+1))
    result += ''.join(row_index(i) for i in range(1,row+1))
    for i in range(1,row+1):
        for n in range(1,row+1):
            result += row_span(i,n)
    for i in range(1,col+1):
        for n in range(1,col+1):
            result += col_span(i,n)
    return result

def html(title:str,style:[str],js:[str],inlineStyle='',inlineJS=''):
    css = '<link rel="stylesheet" type="text/css" href="{i}">'
    javascript = '<script src="{i}"></script>'
    c = '\n    '.join(css.format(i=i) for i in style)
    j = '\n    '.join(javascript.format(i=i) for i in js)
    template = f"""
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width">
    { c }
    { inlineStyle }
    <title>{title}</title>
    { j }
    <meta charset="utf-8">
  </head>
  <body>
    <div id="app" class="grid">
      <div v-bind:class="pos.col + ' ' + pos.row + ' ' + pos.color" v-bind:class="pos.row" v-for="pos in poss">
       {{{{ pos.content }}}}
      </div>
    </div>
    { inlineJS }
  </body>
</html>"""
    return template
def inlineJS(js):
    return f"<script>{js}</script>"

def inlineStyle(style):
    return f"<style>{style}</style>"

__all__ = ["Data","vueJS","grid_style","html","inlineJS","inlineStyle"]
