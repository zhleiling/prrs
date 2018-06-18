# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     recommendate
   Description :
   Author :       zhanglei47
   date：          2018/6/10
-------------------------------------------------
   Change Activity:
                   2018/6/10:
-------------------------------------------------
"""
__author__ = 'zhanglei47'


"""
SELECT COUNT(?movie) SAMPLE(?movie)
        FROM <http://en.dbpedia.org>
        WHERE
        {
          
          ?movie dct:subject ?o .
          ?target rdf:type dbo:Film;
          rdfs:label ?name
          FILTER (?movie != ?target && regex(?name, "superman","i")) .
        } GROUP BY ?movie
        ORDER BY DESC(COUNT(?movie))
"""

from SPARQLWrapper import SPARQLWrapper, JSON

import retrieval

RECOMMEND_FIELDS = {
    'book': ['author', 'publisher'],
    'film': ['director', 'starring'],
    'game': ['developer', 'genre'],
}

PUBLICATION_RETRIEVAL_SELECT = {
    'book': 'SELECT distinct ?publication ?name ?author \n'
            '?releaseDate ?publisher ?numberOfPages\n'
            'WHERE {?publication a dbpedia-owl:Book;\n'
            'dbo:author ?author;\n'
            'dbo:publisher ?publisher;\n'
            'rdfs:label ?name\n' 
            'OPTIONAL {?publication dbp:releaseDate ?releaseDate .}\n'
            'OPTIONAL {?publication dbo:numberOfPages ?numberOfPages .}\n',
    'film': 'SELECT distinct ?thumbnail ?publication ?name ?director \n'
            '?starring ?releaseDate ?distributor ?runtime\n'
            'WHERE {?publication a dbpedia-owl:Film;\n'
            'dbp:director ?director;\n'
            'dbo:starring ?starring;\n'
            'rdfs:label ?name\n'
            'OPTIONAL {?publication dbo:thumbnail ?thumbnail .}\n'
            'OPTIONAL {?publication dbo:releaseDate ?releaseDate .}\n'
            'OPTIONAL {?publication dbo:distributor ?distributor .}\n'
            'OPTIONAL {?publication dbo:runtime ?runtime .}\n',
    'game': 'SELECT distinct ?thumbnail ?publication ?name ?developer \n'
            '?genre ?releaseDate ?publisher \n'
            'WHERE { {?publication a dbpedia-owl:Game } union\n'
            '{?publication a dbpedia-owl:VideoGame}\n'
            '?publication rdfs:label ?name\n'
            'OPTIONAL {?publication dbo:thumbnail ?thumbnail .}\n'
            'OPTIONAL {?publication dbp:developer ?developer .}\n'
            'OPTIONAL {?publication dbo:genre ?genre .}\n'
            'OPTIONAL {?publication dbo:releaseDate ?releaseDate .}\n'
            'OPTIONAL {?publication dbo:publisher ?publisher .}\n',
}

DBPEDIA_RESOURCE_PREFIX = 'http://dbpedia.org/resource/'

def recommend(search_word):
    """

    :param search_word:
    :return: recommen
    """
    retrieval_result = retrieval.retrieval_publication_from_dbpedia(search_word, 10)

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')

    head = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        prefix movie: <http://data.linkedmdb.org/resource/movie/>
        """
    limit = """
    } LIMIT %s
    """ % str(5)

    results = {}
    for publication_type in retrieval.DBPEDIA_PUBLICATION_LIST:
        results[publication_type] = []
        if retrieval_result[publication_type] is not None:
            original_results = retrieval_result[publication_type]
            recommend_field_list = RECOMMEND_FIELDS[publication_type]
            for original_result in original_results:
                keys = original_result.keys()
                # contains all recommend properties
                if len(set(recommend_field_list) - set(keys)) == 0:
                    publication = original_result['publication']
                    recommend_filter = ''
                    for recommend_field in recommend_field_list:
                        recommend_value_list = original_result[recommend_field]
                        #mulitiple value, just use first one
                        recommend_value = recommend_value_list[0]
                        if DBPEDIA_RESOURCE_PREFIX in recommend_value:
                            dbr_key = recommend_value.replace(DBPEDIA_RESOURCE_PREFIX, '')
                            recommend_filter = '%s && ?%s = dbr:%s' % (recommend_filter,
                                                                       recommend_field,
                                                                       dbr_key)
                        else:
                            recommend_filter = '%s && ?%s = "%s"' % (recommend_filter,
                                                                       recommend_field,
                                                                       dbr_key)

                    sparql_filter = 'FILTER (!regex(?name, "%s", "i") ' \
                                    '&& lang(?name) = "en"' \
                                    '%s' \
                                    ') .' \
                                    % (search_word,
                                       recommend_filter)
                    query = '%s\n%s\n%s\n%s' % (head,
                                                retrieval.PUBLICATION_RETRIEVAL_SELECT[publication_type],
                                                sparql_filter, limit)

                    sparql.setQuery(query)
                    sparql.setReturnFormat(JSON)
                    query_result = sparql.query().convert()
                    if len(query_result['results']['bindings']) > 0:
                        merged_result = retrieval.merge_result(query_result['results']['bindings'])
                        results[publication_type].extend(merged_result)
    return results

