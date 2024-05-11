from wjkutil import *
from cachier import cachier

Eng2Chn2 = '''你是一个翻译助手。你将用户的英文输入直接翻译为中文。不要添加任何注解。
英文：{}
中文：'''

# persistent cache for the translation
@cachier()
def ask3(msg):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key="xxxxx")
    response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
            {"role": "user", "content": msg},
        ],
    )
    return response.choices[0].message.content

@cachier()
def translate(text):
    return ask3(Eng2Chn2.format(text))


texts = read_file("body.tex")
texts = texts.splitlines()

def merge_pair(texts, begin, end):
    ret = []
    matched = False
    buf = []
    for line in texts:
        line_s = line.strip()
        if line_s.startswith(begin):
            matched = True
        if matched:
            buf.append(line)
        else:
            ret.append(line)
        if line_s == end:
            assert matched is True
            matched = False
            ret.append('\n'.join(buf))
    return ret

texts = merge_pair(texts, r"\begin{center}", r"\end{center}")
texts = merge_pair(texts, r"\footnotetext{", r"}")

skips = [r"\begin{itemize}", r'\end{itemize}', r"\begin{center}", r'\footnotetext{', r'\includegraphic', r'\begin{enumerate}', r'\end{enumerate}', r'${ }^{', r"\setcounter"]

# count = 20

latex_one = re.compile(r'^\\([^{]+){(.+)}$')
super_script = re.compile(r'\^([0-9]+)')

for i in range(len(texts)):
    # debug
    # if count <= 0:
    #     continue
    line = texts[i]
    line_s = line.strip()
    if len(line) == 0:
        continue
    skip = False
    for s in skips:
        if line_s.startswith(s):
            skip = True
    if skip:
        continue
    print(f"【T】Translating: {line}")
    if m := latex_one.match(line_s):
        translated = '\\' + f'{m.group(1)}{{{translate(m.group(2))}}}'
    elif line_s.startswith("\\item"):
        part = line_s.removeprefix("\\item")
        translated = '\\' + f'item {translate(part)}'
    else:
        translated = translate(line)
    translated = super_script.sub(r"\\textsuperscript{\1}", translated)
    print(f"【R】Result: {translated}")
    texts[i] = f'% {line}\n{translated}'
    # count -= 1


write_file("body_translated.tex", '\n'.join(texts))

# =====================
# !!! deprecated below !!!
# =====================

# # pip install texsoup
# from TexSoup import TexSoup

# # load
# main = TexSoup(read_file('main.tex'))

# from TexSoup.utils import TC
# from TexSoup.utils import Token

# skip = ['documentclass', 'usepackage', 'graphicspath', 'hypersetup', 'urlstyle', 'author', 'date']

# count = 10
# # modify
# for node in main.document:
#     if count <= 0: continue
#     if type(node) is Token:
#         if node.category == TC.Comment:
#             continue
#         else:
#             print(f"Translating: ")
#     else:
#         if node.name in skip:
#             continue
#         else:
#             print(node.name)
#     count -= 1

# # save
# write_file("main_translated.tex", str(main))



Eng2Chn3 = '''你是一个翻译助手。你将用户的英文输入直接翻译为中文。尽可能少地使用英文单词。
英文：{}
中文：'''

#  Do not output other words. Do not add any remarks or annotations or comments or notes.
# main prompt for translation
Eng2Chn = """You are a English to Chinese translator. You translate user's English input to Chinese and directly output the result. Try your best and output as less English as possible. 你需要输出简体中文.
English: {}
Chinese: """


@cachier()
def ask(msg):
    from openai import OpenAI
    client = OpenAI(api_key = "none", base_url="http://222.20.126.133:8000/v1")
    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "user", "content": msg}
        ]
    )
    return response.choices[0].message.content

@cachier()
def ask2(msg):
    from openai import OpenAI
    client = OpenAI(api_key = "none", base_url="http://172.19.192.5:8000/v1")
    response = client.chat.completions.create(
        model="chatglm3-6b",
        messages=[
            {"role": "user", "content": msg}
        ]
    )
    return response.choices[0].message.content


def translate2(msg):
    from openai import OpenAI
    client = OpenAI(api_key = "none", base_url="http://172.19.192.5:8000/v1")
    response = client.chat.completions.create(
        model="haoranxu/ALMA-7B-R",
        messages=[
            {"role": "user", "content": f"Translate this from English to Chinese:\nEnglish: {msg}\nChinese:"}
        ]
    )
    return response.choices[0].message.content


# curl -X POST http://localhost:11434/api/generate -d '{
#   "model": "llama3",
#   "prompt":"Why is the sky blue?"
#  }'

def ask4(msg):
    import requests
    return requests.post('http://172.19.192.5:11434/api/generate', json={
        "model": "llama3:8b-instruct-fp16",
        "prompt":msg,
        "stream": False,
        "options": {
        "temperature": 0.8
    }}).json()["response"]

# print(ask4(Eng2Chn3.format('''Science can be thought of as the combination of three essential things: (1) a communal collection of knowledge (both facts/data and theories); (2) a method of evaluating the efficacy of scientific theories by comparing the predictions of those theories to observation/experiment; and (3) an attitude of skeptical inquiry and the belief that all scientific knowledge is provisional and subject to revision when confronted with new evidence. (A popular alternative breakdown of the "norms" of science, emphasizing its sociological nature, is Merton's "cudos", first introduced in 1942: communalism, universality, disinterestedness, originality, and skepticism. ${ }^{1}$ ) This breakdown of science into a body of knowledge, a method, and an attitude is useful in assessing the "scientific" content of any given behavior. If any one of these three pillars of science is missing from an activity, one cannot claim that the activity is scientific.''')))
