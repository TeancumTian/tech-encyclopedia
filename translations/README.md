# 中英文内容维护 / Translation maintenance

中文书稿仍以 `domains/*.md`、`front/*.md` 和 `data/src/*.txt` 为来源。英文保存在本目录，普通构建不调用模型、翻译网站或网络服务。学习记录、用户笔记及备份文件不进入翻译流程。

- `en.auto.json`：本机 Qwen3.5（9B / 4B）辅助生成的全书正文和 SVG 标签译文。按中文原句索引，保留词条 ID、交叉引用、日期与公式。
- `ui.en.json`：界面、课程、小测与实验提示译文。
- `en.json`：编辑复核与术语覆盖，优先级最高，包括原书已有英文名称、主界面文案、59 条原理说明和 17 篇简介，以及核心条目的机制说明、后部章节和长篇核实清单。
- `ui.source.json`：从界面源码提取的文案、插值模板和源文件摘要。正文覆盖从书稿自动计算；中文修改后，旧译文不会错误匹配到新句子。

构建将这些文件合并为 `build/web/en.json`，并生成 183 份英文 SVG 和英文封面。模型与其权重不随网站分发。英文是机器辅助翻译与编辑复核的版本，不代表重新核实原书全部史实；可用中英对照查看中文来源。PDF 继续使用原中文书稿。

## 修改内容

1. 修改中文原稿或网页文案。
2. 界面有改动时，运行 `npm install --prefix tools/localization`，再运行 `node scripts/extract_ui.cjs` 更新文案清单。这个解析工具只在编辑时使用，网站和 CI 构建不需要 npm 包。
3. 补齐相应英文。术语或译法修订写入 `en.json`；保留 `[[entry-id|label]]` 的 ID，只翻译 label。界面模板中的 `{0}` 等占位符必须完整保留，英文中可以调整其顺序。
4. 运行 `make web-check`，核对三种语言模式、长标题、正文链接、图解、动态反馈和至少一个手机尺寸。漏译、未更新的界面清单或缺失的书稿引用会阻止通过检查。

脚本 `scripts/translate_english.py` 只供可恢复的本机批量编辑使用，默认连接 `localhost:11434` 的既有 Ollama 模型，不会从网页运行。它需要显式提供源文清单和输出文件；翻译完成后仍须经过覆盖检查与编辑复核。可用 `--endpoint` 指定其他本机端口，脚本拒绝非本机地址；`--workers` 可设置并发请求数，检查点始终由单个协调器原子写入。运行期间新增的编辑覆盖会自动从待译队列跳过。

```bash
# 只提取当前原稿，不覆盖已验证的网站产物
python3 scripts/build_web.py --inventory build/translation/source.json
python3 scripts/translate_english.py --source build/translation/source.json --output translations/en.auto.json
```

批量助手跳过已有正文译文、编辑覆盖和界面清单；界面文案由编辑单独维护。失败段落输出到 `build/translation/retry.json`，修订后须重新运行严格检查。

## 阅读与进度

中文、English、中英对照共用同一组内容 ID、已读状态、收藏、笔记、错题与复习安排。语言偏好作为 v2 进度中的 `prefs.language` 保存，旧存档默认使用中文。导入会保留当前页面的语言选择；个人笔记在所有模式下原样显示。

In English mode, the complete manuscript, interface, lessons and diagrams are available in English. Parallel mode places the English text below each Chinese passage and offers an expandable English diagram. Both languages share the same reading records; personal notes are never automatically translated.
