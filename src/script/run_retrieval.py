# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sparql_query_demo
   Description :
   Author :       zhanglei47
   date：          2018/6/9
-------------------------------------------------
   Change Activity:
                   2018/6/9:
-------------------------------------------------
"""
__author__ = 'zhanglei47'

import sys
sys.path.append('../model')
import retrieval


keyword = sys.argv[1]


results = retrieval.retrieval_publication_from_dbpedia(keyword)

import json
#print(json.dumps(results))

html_format_result = retrieval.html_format_dbpedia_results(keyword, results)

print(html_format_result)

