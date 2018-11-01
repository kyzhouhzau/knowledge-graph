# -*- coding: utf-8 -*-
import scrapy
from OMIMPROJECT.items import OmimprojectItem
from bs4 import BeautifulSoup

def get_url():
    path = "./data/mim.txt"
    urls=[]
    count=0
    with open(path,'r') as rf:
        for line in rf:
            count+=1
            line = line.strip()
            urls.append(line)
        return urls

class OmimSpider(scrapy.Spider):
    name = "omim"
    allowed_domains = ["omim.org"]
    def start_requests(self):
        base_url = 'http://omim.org/entry/'
        nums = get_url()
        nums = sorted(nums)
        for i,num in enumerate(nums):
            url = base_url+str(num)
            yield self.make_requests_from_url(url)


    def parse(self, response):
        url = response.url
        MIM = url.split('/')[-1]
        item = OmimprojectItem()
        soup = BeautifulSoup(response.text, 'lxml')
        all = soup.select('#allelicVariantsFold > div')
        for div in all:
            divdiv = list(div.select("div"))
            if len(divdiv) != 0:
                disease = divdiv[0].text.strip().split('\n')[-1]
                gene = divdiv[1].text.strip().split('\n')[0].split(',')[0]
                mutation = divdiv[1].text.strip().split('\n')[0].split(',')[1:]
                mutation = ','.join(mutation)
                text = divdiv[3].text.strip()
                item["disease"]=disease
                item["MIM"]=MIM
                item["gene"]=gene
                item["mutation"]=mutation
                item["article"]=text
                yield item








