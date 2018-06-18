# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dbpedia_sparql_run_demo
   Description :
   Author :       zhanglei47
   date：          2018/6/17
-------------------------------------------------
   Change Activity:
                   2018/6/17:
-------------------------------------------------
"""
__author__ = 'zhanglei47'


from SPARQLWrapper import SPARQLWrapper, JSON


if __name__ == '__main__':

    sparql = SPARQLWrapper('http://dbpedia.org/sparql')

    head = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    prefix movie: <http://data.linkedmdb.org/resource/movie/>
    """

    sql = """
    SELECT COUNT(?movie) SAMPLE(?movie)
        FROM <http://en.dbpedia.org>
        WHERE
        {
          dbr:A_Trip_to_the_Moon rdf:type ?o .
          ?movie rdf:type ?o 
          FILTER (?movie != dbr:A_Trip_to_the_Moon) .
        } GROUP BY ?movie
        ORDER BY DESC(COUNT(?movie))
    """

    query = '%s\n%s\n' % (head, sql,)
    sparql.setQuery(query)
    sparql.setTimeout(6000)
    sparql.setReturnFormat(JSON)
    query_result = sparql.query().convert()

    print(query_result)