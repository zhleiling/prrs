# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py
   Description :
   Author :       zhanglei47
   date：          2018/6/17
-------------------------------------------------
   Change Activity:
                   2018/6/17:
-------------------------------------------------
"""
__author__ = 'zhanglei47'


import sys
sys.path.append('./model')
import retrieval, recommend

if __name__ == '__main__':
    search_word = sys.argv[1]
    retrieval_result = retrieval.retrieval_publication_from_dbpedia(search_word)
    retrieval_html_result = retrieval.html_format_dbpedia_results(search_word, retrieval_result)
    with open('../result/retrieval.html', 'w') as of:
        of.write(retrieval_html_result)
        of.flush()

    recommend_result = recommend.recommend(search_word)
    recommend_html_result = retrieval.html_format_dbpedia_results(search_word, recommend_result, True)
    with open('../result/recommend.html', 'w') as of:
        of.write(recommend_html_result)
        of.flush()
