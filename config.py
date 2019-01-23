import os

TEXT_MIN_WORDS = 100
SUMMARY_MIN_WORDS = 35
TIMEOUT = 60

AUTHORS = os.environ.get('AUTHORS',"u/aaa u/bbb u/ddd")
COMMENT_HEADER = """### Resumen de la noticia\n\n"""
COMMENT_FOOTER = """\n\n---\n\n[Source Code](https://github.com/pastine/resumidor-estatal) | [Tell me how to improve](https://github.com/pastine/resumidor-estatal/issues) | Created by: """+AUTHORS
