# 《How to write a good scientific paper》 by Chris A. Mark 中文版



### 翻译路线

1. 使用 [mathpix](https://mathpix.com/) 将原始 PDF 文件（`original.pdf`）翻译成 Overleaf LaTeX 项目。
2. 下载 LaTeX 项目，获取 `main.tex` 文件，并将正文部分手动分割到 `body.tex`。
3. 使用 `translator.py` 将 `body.tex` 翻译成 `body_translated.tex`。
4. 手动检查并修改 `body_translated.tex` 得到 `body_translated_final.tex`。
5. 编译 LaTeX 项目，生成翻译后的 `main.pdf`。

1. Use [mathpix](https://mathpix.com/) to translate the original PDF file (`original.pdf`) into an overleaf latex project.
2. download the latex project, get the `main.tex`, and manually split body parts to `body.tex`
3. use `translator.py` to translate `body.tex` to `body_translated.tex`.
4. Manually check and modify `body_translated.tex` and get `body_translated_final.tex`
5. Compile the latex project and get the translated `main.pdf`
