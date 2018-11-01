#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
from SPARQLWrapper import  JSON
from pyecharts import Graph
import jieba

from AGAC_KGQA.settings  import diseases,drugs,sparql
class natural2sparql(object):
    def __init__(self,question):
        self.question = question
        self.sparql_sentence1 = self.convert_nl2sparql()
    def convert_nl2sparql(self):
        baserule_drug1 = """
        SELECT ?drug  ?gene ?mutation
        WHERE {{{{
        function:LOF :cause {disease} .
        ?mutation :cause function:LOF;
                    :theme ?gene .
        {drug} :agonist ?gene .}}
        UNION
        {{
        function:GOF :cause {disease} .
        ?mutation :cause function:GOF;
                    :theme ?gene .
        {drug} :antigonist ?gene .}}}}
        """
        baserule_drug2 = """
        SELECT ?disease  ?gene  ?mutation
        WHERE {{{{
        function:LOF :cause {disease} .
        ?mutation :cause function:LOF;
                    :theme ?gene .
        {drug} :agonist ?gene .}}
        UNION
        {{
        function:GOF :cause {disease} .
        ?mutation :cause function:GOF;
                    :theme ?gene .
        {drug} :antigonist ?gene .}}}}
        """
        #self.question 需要被解析
        seg_list = jieba.cut(self.question, cut_all=False)
        disease="?disease"
        drug="?drug"
        drug_or_disease=''
        baserule_drug=''
        for word in seg_list:
            dic111 = list(map(lambda i:i.lower(), diseases))
            dic222 = list(map(lambda i:i.lower(), drugs))
            if word.lower() in dic111:
                disease="disease:"+word
                drug_or_disease=disease
                baserule_drug = baserule_drug1
            elif word.lower() in dic222:
                drug = "drug:"+word
                drug_or_disease=drug
                baserule_drug = baserule_drug2
        self.drug_or_disease=drug_or_disease
        self.action="not_known"

        sparql_sentence1 = baserule_drug.format(disease=disease,drug=drug)
        return sparql_sentence1




def jena_endpoint(sparql_sentence):
    sql="""
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX gene: <http://www.agac.com/gene/>
        PREFIX mutation: <http://www.agac.com/mutation/>
        PREFIX disease: <http://www.drugbank.com/disease/>
        PREFIX drug: <http://www.drugbank.com/drug/>
        PREFIX function: <http://www.agac.com/function/>
        PREFIX : <http://www.agac.com/schema/>
        {}
        """.format(sparql_sentence)
    sql = sql.replace('\n'," ")
#     sql ="""
#     PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX gene: <http://www.agac.com/gene/>
#     PREFIX mutation: <http://www.agac.com/mutation/>
#     PREFIX disease: <http://www.drugbank.com/disease/>
#     PREFIX drug: <http://www.drugbank.com/drug/>
#     PREFIX function: <http://www.agac.com/function/>
#     PREFIX : <http://www.agac.com/schema/>
#     SELECT ?s ?p ?o
#     WHERE {?s ?p ?o }
# """
    sparql.setQuery(sql)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result

def parse_jena_result( result):
    resultdir = result["results"]["bindings"]
    if len(resultdir)==0:
        return None
    else:
        return resultdir
def bulild_html(result,action,disease):
    links = []
    nodes = []
    try:
        for triples in result:
            if 'drug' in triples.keys():
                s = "drug:"+triples['drug']['value'].split('/')[-1]
                p = "action:" + action
                o = "gene:" + triples['gene']['value'].split('/')[-1]
                pp = "action:" + "cure"
                oo = disease
            else:
                s = "disease:" + triples['disease']['value'].split('/')[-1]
                p = "action:" + "relate_to"
                o = "gene:" + triples['gene']['value'].split('/')[-1]
                pp = "action:" + "cause"
                oo = "mutation:" + triples['mutation']['value'].split('/')[-1]
            mm = {"name": s, "symbolSize": 20}
            nn = {"name": o, "symbolSize": 20}
            kk = {"name":oo,"symbolSize":20}
            if mm not in nodes:
                nodes.append(mm)
            if nn not in nodes:
                nodes.append(nn)
            if kk not in nodes:
                nodes.append(kk)
            links.append({"source": s, "value": p, "target": o})
            links.append({"source": o, "value": pp, "target": oo})
        graph = Graph("基因-疾病-药物")
        graph.add("", nodes, links, graph_repulsion=400)
        graph.render(path=r"E:\KG_DEMO\AGAC_KGQA_PART\kgqa\templates\kgqa\render.html")
    except TypeError:
        pass

def question(question):
    q = natural2sparql(question)
    sql1=q.sparql_sentence1
    print(sql1)
    result1 = jena_endpoint(sql1)
    resultdir1 = parse_jena_result(result1)
    bulild_html(resultdir1,q.action,q.drug_or_disease)
    # return resultdir1
#
# q = "which drug can be used to cure ALZHEIMER?"
# question(q)



