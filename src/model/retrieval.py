# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     retrieval
   Description :
   Author :       zhanglei47
   date：          2018/6/10
-------------------------------------------------
   Change Activity:
                   2018/6/10:
-------------------------------------------------
"""
__author__ = 'zhanglei47'


from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA_PUBLICATION_LIST = ['book', 'game', 'film']

PUBLICATION_RETRIEVAL_SELECT = {
    'book': 'SELECT distinct ?publication ?name ?author \n'
            '?releaseDate ?publisher ?numberOfPages\n'
            'WHERE {?publication a dbpedia-owl:Book;\n' 
            'rdfs:label ?name\n' 
            'OPTIONAL {?publication dbo:author ?author .}\n'
            'OPTIONAL {?publication dbp:releaseDate ?releaseDate .}\n'
            'OPTIONAL {?publication dbo:publisher ?publisher .}\n'
            'OPTIONAL {?publication dbo:numberOfPages ?numberOfPages .}\n',
    'film': 'SELECT distinct ?thumbnail ?publication ?name ?director \n'
            '?starring ?releaseDate ?distributor ?runtime\n'
            'WHERE {?publication a dbpedia-owl:Film;\n'
            'rdfs:label ?name\n' \
            'OPTIONAL {?publication dbo:thumbnail ?thumbnail .}\n'
            'OPTIONAL {?publication dbp:director ?director .}\n'
            'OPTIONAL {?publication dbo:starring ?starring .}\n'
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


def retrieval_publication_from_dbpedia(query_word, limit_num=100):
    """
    retrieval_publication_from_dbpedia
    :param query_word:
    :param limit_num:
    :return: retrival result from dbpedia
    """
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')

    head = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    prefix movie: <http://data.linkedmdb.org/resource/movie/>
    """

    sparql_filter = 'FILTER (regex(?name, "%s", "i") ' \
                    '&& lang(?name) = "en"' \
                    ') .'\
                    % query_word

    limit = """
    } LIMIT %s
    """ % str(limit_num)
    results = {}

    for publication_type in DBPEDIA_PUBLICATION_LIST:
        select = PUBLICATION_RETRIEVAL_SELECT[publication_type]

        query = '%s\n%s\n%s\n%s' % (head, select, sparql_filter, limit)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        query_result = sparql.query().convert()
        merged_result = merge_result(query_result['results']['bindings'])
        results[publication_type] = merged_result
    return results


def html_format_dbpedia_results(search_word, results, recommend_flag=False):
    """
    html_format_dbpedia_results
    :param search_word:
    :param results:
    :return:
    """
    html_arr_res = list()
    html_arr_res.append('<html><head><title>Search result:</head></title>')
    if recommend_flag:
        html_arr_res.append('<body><h1>Recommend for you by searching"{}":</h1>'.format(search_word))
    else:
        html_arr_res.append('<body><h1>Result for "{}":</h1>'.format(search_word))

    # books
    html_arr_res.append('<h2>1、matching books:</h2>')
    html_arr_res.append('<table border="1">')
    html_arr_res.append('<tr>')
    html_arr_res.append('<th>bookName</th>')
    html_arr_res.append('<th>author</th>')
    html_arr_res.append('<th>publisher</th>')
    html_arr_res.append('<th>releaseDate</th>')
    html_arr_res.append('<th>numberOfPages</th>')
    html_arr_res.append('</tr>')

    for publication_type in DBPEDIA_PUBLICATION_LIST:
        if publication_type not in results:
            results[publication_type] = []
    for query_result in results['book']:
        if 'publication' in query_result:
            html_arr_res.append('<tr>')

            # publication
            assert(len(query_result['publication']) == 1)
            url = query_result['publication'][0]
            assert (len(query_result['name']) == 1)
            name = query_result['name'][0]
            html_arr_res.append('<td><a href="{}">{}</a></td>'.format(url, name))
            # author
            html_arr_res.append('<td>')
            if 'author' in query_result:
                author_urls = query_result['author']
                for author_url in author_urls:
                    author_name = author_url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(author_url, author_name))
            html_arr_res.append('</td>')
            # publisher
            html_arr_res.append('<td>')
            if 'publisher' in query_result:
                publisher_urls = query_result['publisher']
                for publisher_url in publisher_urls:
                    publisher_name = publisher_url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(publisher_url, publisher_name))
            html_arr_res.append('</td>')
            # releaseDate
            html_arr_res.append('<td>')
            if 'releaseDate' in query_result:
                release_dates = query_result['releaseDate']
                for release_date in release_dates:
                    html_arr_res.append('{}<br/>'.format(release_date))
            html_arr_res.append('</td>')
            # numberOfPages
            html_arr_res.append('<td>')
            if 'numberOfPages' in query_result:
                number_of_pages = query_result['numberOfPages']
                for numberOfPages in number_of_pages:
                    html_arr_res.append('{}<br/>'.format(numberOfPages))
            html_arr_res.append('</td>')

            html_arr_res.append('</tr>')
    html_arr_res.append('</table>')

    # films
    html_arr_res.append('<h2>2、matching films:</h2>')
    html_arr_res.append('<table border="1">')
    html_arr_res.append('<tr>')
    html_arr_res.append('<th>thumbnail</th>')
    html_arr_res.append('<th>filmName</th>')
    html_arr_res.append('<th>director</th>')
    html_arr_res.append('<th>starring</th>')
    html_arr_res.append('<th>distributor</th>')
    html_arr_res.append('<th>releaseDate</th>')
    html_arr_res.append('<th>runtime(seconds)</th>')
    html_arr_res.append('</tr>')

    for query_result in results['film']:
        if 'publication' in query_result:
            html_arr_res.append('<tr>')

            # thumbnail
            html_arr_res.append('<td>')
            if 'thumbnail' in query_result:
                assert(len(query_result['thumbnail']) == 1)
                thumbnail = query_result['thumbnail'][0]
            else:
                thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/9/95/Toicon-icon-sharp-corners-film.svg'
            html_arr_res.append('<img src="{}" height="60px">'.format(thumbnail))
            html_arr_res.append('</td>')
            # publication
            assert (len(query_result['publication']) == 1)
            url = query_result['publication'][0]
            assert (len(query_result['name']) == 1)
            name = query_result['name'][0]
            html_arr_res.append('<td><a href="{}">{}</a></td>'.format(url, name))
            # director
            html_arr_res.append('<td>')
            if 'director' in query_result:
                urls = query_result['director']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # starring
            html_arr_res.append('<td>')
            if 'starring' in query_result:
                urls = query_result['starring']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # distributor
            html_arr_res.append('<td>')
            if 'distributor' in query_result:
                urls = query_result['distributor']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # releaseDate
            html_arr_res.append('<td>')
            if 'releaseDate' in query_result:
                release_dates = query_result['releaseDate']
                for release_date in release_dates:
                    html_arr_res.append('{}<br/>'.format(release_date))
            html_arr_res.append('</td>')
            # runtime
            html_arr_res.append('<td>')
            if 'runtime' in query_result:
                runtimes = query_result['runtime']
                for runtime in runtimes:
                    html_arr_res.append('{}<br/>'.format(runtime))
            html_arr_res.append('</td>')

            html_arr_res.append('</tr>')
    html_arr_res.append('</table>')

    # games
    html_arr_res.append('<h2>3、matching games:</h2>')
    html_arr_res.append('<table border="1">')
    html_arr_res.append('<tr>')
    html_arr_res.append('<th>thumbnail</th>')
    html_arr_res.append('<th>gameName</th>')
    html_arr_res.append('<th>developer</th>')
    html_arr_res.append('<th>genre</th>')
    html_arr_res.append('<th>publisher</th>')
    html_arr_res.append('<th>releaseDate</th>')
    html_arr_res.append('</tr>')

    for query_result in results['game']:
        if 'publication' in query_result:
            html_arr_res.append('<tr>')

            # thumbnail
            html_arr_res.append('<td>')
            if 'thumbnail' in query_result:
                assert (len(query_result['thumbnail']) == 1)
                thumbnail = query_result['thumbnail'][0]
            else:
                thumbnail = 'https://upload.wikimedia.org/wikipedia/commons/6/63/Game_Icon.png'
            html_arr_res.append('<img src="{}" height="60px">'.format(thumbnail))
            html_arr_res.append('</td>')
            # publication
            assert (len(query_result['publication']) == 1)
            url = query_result['publication'][0]
            assert (len(query_result['name']) == 1)
            name = query_result['name'][0]
            html_arr_res.append('<td><a href="{}">{}</a></td>'.format(url, name))
            # developer
            html_arr_res.append('<td>')
            if 'developer' in query_result:
                urls = query_result['developer']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # genre
            html_arr_res.append('<td>')
            if 'genre' in query_result:
                urls = query_result['genre']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # publisher
            html_arr_res.append('<td>')
            if 'publisher' in query_result:
                urls = query_result['publisher']
                for url in urls:
                    text = url.split('/')[-1]
                    html_arr_res.append('<a href="{}">{}</a><br/>'.format(url, text))
            html_arr_res.append('</td>')
            # releaseDate
            html_arr_res.append('<td>')
            if 'releaseDate' in query_result:
                release_dates = query_result['releaseDate']
                for release_date in release_dates:
                    html_arr_res.append('{}<br/>'.format(release_date))
            html_arr_res.append('</td>')

            html_arr_res.append('</tr>')
    html_arr_res.append('</table>')

    html_arr_res.append('</body></html>')
    return '\n'.join(html_arr_res)


def merge_result(query_result):
    """
    merge multiple values in optional fields
    :param query_result:
    :return:
    """
    merged_result = {}
    for item in query_result:
        key = item['publication']['value']
        if key not in merged_result:
            merged_result[key] = {}
            for col, obj in item.items():
                value = obj['value']
                merged_result[key][col] = [value]
        else:
            orig_values = merged_result[key]
            for col, obj in item.items():
                value = obj['value']
                if col not in orig_values:
                    orig_values[col] = list()
                if value not in orig_values[col]:
                    orig_values[col].append(value)
                    merged_result[key] = orig_values
    return merged_result.values()
