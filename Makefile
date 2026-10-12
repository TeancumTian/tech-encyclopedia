# 用法：make pdf / make sample / make check / make clean
# 默认用系统 python3；也可以 make pdf PYTHON=.venv/bin/python
PYTHON ?= python3

.PHONY: help deps pdf pdf-en sample sample-en check clean entries index-keys web web-serve web-check

help:
	@echo 'make deps    安装 Python 依赖' 
	@echo 'make pdf     出全书 PDF -> build/近现代科技百科全书-全书.pdf'
	@echo 'make sample  出样章 PDF -> build/样章.pdf'
	@echo 'make pdf-en  出英文版全书 PDF -> build/tech-encyclopedia-en.pdf'
	@echo 'make sample-en  出英文样章 PDF -> build/sample-en.pdf'
	@echo 'make check   检查 SVG / JSON / 路径'
	@echo 'make web     构建互动学习网页 -> build/web/'
	@echo 'make web-serve  构建并打开本机预览服务（4173）'
	@echo 'make web-check  检查书稿、网页与互动模型'
	@echo 'make clean   删除 build/'

deps:
	$(PYTHON) -m pip install -r requirements.txt

pdf:
	$(PYTHON) tools/build_pdf.py

sample:
	$(PYTHON) tools/build_pdf.py --sample computing

# English edition: same manuscript, typeset through translations/*.json; fails if any line lacks a translation.
pdf-en:
	$(PYTHON) tools/build_pdf.py --lang en

sample-en:
	$(PYTHON) tools/build_pdf.py --lang en --sample computing

check:
	$(PYTHON) tools/check_book.py --quiet
	$(PYTHON) tools/filler_check.py --quiet

entries:
	$(PYTHON) tools/compile_entries.py

index-keys:
	$(PYTHON) tools/make_index_keys.py

clean:
	rm -rf build

web:
	$(PYTHON) scripts/build_web.py

web-serve: web
	$(PYTHON) scripts/serve_web.py

web-check: check web
	@for file in web/*.js; do node --check "$$file" || exit 1; done
	$(PYTHON) -m unittest discover -s tests -p "test_*.py"
	node --test tests/*.test.js
