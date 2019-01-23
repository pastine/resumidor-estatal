import os

TEXT_MIN_WORDS = 100
SUMMARY_MIN_WORDS = 35
TIMEOUT = 60

AUTHORS = os.environ.get('AUTHORS',"u/aaa u/bbb u/ddd")
COMMENT_HEADER = """### Resumen de la noticia\n\n"""
COMMENT_FOOTER = """\n\n---\n\nCreated by: """+AUTHORS+""" | [Source Code](https://github.com/pastine/resumidor-estatal)"""
