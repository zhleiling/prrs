# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     run_recommend
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
sys.path.append('../model')
import recommend
import retrieval


keyword = sys.argv[1]


results = recommend.recommend(keyword)

import json
#print(json.dumps(results))

html_format_result = retrieval.html_format_dbpedia_results(keyword, results)

print(html_format_result)