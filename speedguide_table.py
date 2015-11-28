#!/usr/bin/env python3
# coding: utf-8
from pyquery import PyQuery as pq
from lxml import etree
import urllib
from urllib import parse
import html2text
import re
import lxml
import sys
import ipdb
import traceback
import sqlite3
from collections import OrderedDict
from my_utils import ulog,uprint
import itertools
from infix_operator import Infix
from postgres_utils import dict2hstore, hstore2dict


def getStartIdx():
    global startTrail
    if startTrail:
        return startTrail.pop(0)
    else:
        return 0

def sql(query:str, var=None):
    global conn
    csr=conn.cursor()
    try:
        if var:
            rows = csr.execute(query,var)
        else:
            rows = csr.execute(query)
        if not query.startswith('SELECT'):
            conn.commit()
        if query.startswith('SELECT'):
            return rows.fetchall()
        else:
            return
    except sqlite3.Error as ex:
        print(ex)
        raise ex

def elmToMd(elm:lxml.html.Element, ignore_links=True, ignore_images=True, 
        ignore_emphasis=True):
    html = etree.tostring(elm).decode('utf-8')
    h = html2text.HTML2Text()
    h.body_width=0
    h.ignore_emphasis = ignore_emphasis
    h.ignore_images= ignore_images
    h.ignore_links= ignore_links
    return h.handle(html)                                                               
def urlChangePath(baseUrl, path):
    assert not re.match('http|https', path)
    sp= parse.urlsplit(baseUrl)
    assert sp.scheme and sp.netloc
    return parse.SplitResult(sp.scheme, sp.netloc, path, '','').geturl()


def surrDQuote(s:str)->str:
    return '"'+s+'"'


def abgnac_format(v:str)->str:
    dic = OrderedDict([('a',0),('b',0),('g',0),('n',0),('ac',0)])
    for l in v.splitlines(): 
        m = re.match(r'802\.11(\w+)', l)
        if m:
            dic[m.group(1)]=1
    ret=""
    for k,v in dic.items():
        if v:
            if k=='ac':
                ret += '+ac'
            else:
                ret += k
    assert re.match(r'a?b?g?n?(\+ac)?', ret)
    return ret

def findLineIdxWith(lineList:[str], beginIdx:int, cond)->int:
    return next((i for i,_ in enumerate(lineList[beginIdx:],beginIdx) 
        if cond(_)), -1)

def convertUserPassword(s:str)->str:
    """
    'Default admin password: |  (blank)'
    """
    if s.isalnum():
        return s
    elif s=='(blank)':
        return ''
    elif s=='n/a':
        return ''
    else:
        ulog('s="%s"'%s)
        return s

def scrapeDetails(curUrl):
    global prevTrail
    ulog('curUrl= '+curUrl)
    try:
        d= pq(curUrl)
        md = elmToMd(d('#content')[0],True,True)
        # get device description
        mdl = md.splitlines()
        i = next(i for i,_ in enumerate(mdl) if _.strip().startswith('Home'))
        # step to non empty line
        brmd = [_.strip() for _ in mdl[i].split('» ')]
        brand = brmd[3]
        model = brmd[4].replace('Details','').strip()

        # get product Name
        i =findLineIdxWith(mdl,i+1,lambda _:_.strip().startswith('details:'))
        prodName = mdl[i].split(' |' )[1].strip()
        # "Dual-band wireless-AC3100 gigabit router"
        i = findLineIdxWith(mdl,i+1,
                lambda _:_.strip().startswith('hardware type:'))
        category = mdl[i].split(' | ')[1].strip()
        # "Wireless Router"

        # find empty line after details
        i = findLineIdxWith(mdl,i+1,lambda _:not _.strip())
        # find non empty line
        i = findLineIdxWith(mdl,i+1,lambda _:_.strip())
        j = findLineIdxWith(mdl,i+1,
                lambda _:re.match(r'All .+ products$',_.strip()))
        description='\n'.join(_.strip() for _ in mdl[i:j] if _.strip())
        default_user_name,default_password,wifi_proto,availability,\
                product_page,hw_fla1_amount,hw_ram1_amount = \
                None,None,None,None,None,None,None

        trs = d('.tblight tr')
        pr=OrderedDict()
        for tr in trs:
            l = elmToMd(tr,False,False)
            if ' | ' not in l:
                continue
            n,v = [_.strip() for _ in l.split(' | ',1)]
            v = '\n'.join(_.strip() for _ in v.splitlines())
            assert n not in pr
            n = n.rstrip(':')
            if v:
                v0 = v[0]
                if v0=='!':
                    yn = re.search(r'!\[(.+?)\]', v).group(1)
                    if yn=='yes': v= "true"
                    elif yn=='no': v = "false"
                    else: ipdb.set_trace(); uprint(yn)
                elif v0 =='<':
                    v = re.search(r'<(.+?)>',v).group(1).strip()
                    # "<http://router.asus.com>"
                elif v0 == '[':
                    hreftitle = re.search(r'\((.+?)(?<!\\)\)', v).group(1)
                    v = hreftitle.split()[0]
                    v = v.replace('\\', '')
                else:
                    """
                    'Transmit Power: |  +30 dBm'
                    'Receiver Sensitivity: |  -76 dBm'
                    'Street price: |  $52'
                    'Default admin password: |  (blank)'
                    """
                    if v0.isalnum() or v0 in "+-$" or (v0=='(' and v[-1]==')') :
                        pass
                    else:
                        ipdb.set_trace()
            else:
                pass
            pr[n] = v
            if n== 'Default admin username':
                default_user_name = convertUserPassword(v)
            elif n== 'Default admin password':
                default_password = convertUserPassword(v)
            elif n=='WiFi standards supported':
                wifi_proto = abgnac_format(v)
            elif n== 'Availability':
                availability = v
            elif n == 'Product page':
                product_page = v
            elif n=='Flash Memory':
                assert re.match(r'[\d]*\.?\d+\s*(Mb|Kb)',v,re.I)
                hw_fla1_amount = v
            elif n== 'RAM':
                assert re.match(r'[\d]*\.?\d+\s*(Mb|Kb)',v,re.I)
                hw_ram1_amount = v
            else:
                pr[n]=v

        props_hstore = dict2hstore(pr)
        img= d('a.piframe img')[0]
        image_url=urlChangePath(d.base_url,img.attrib['src'])
        trailStr = str(prevTrail)

        sql("INSERT OR REPLACE INTO TFiles(brand,model,prod_name,category"
            ", default_user_name, default_password, wifi_proto, availability"
            ", description, product_page, hw_fla1_amount, hw_ram1_amount"
            ", image_url, props_hstore, tree_trail) VALUES "
            "(:brand,:model,:prodName,:category"
            ",:default_user_name,:default_password,:wifi_proto,:availability"
            ",:description,:product_page,:hw_fla1_amount,:hw_ram1_amount"
            ",:image_url,:props_hstore,:trailStr)", locals())
        uprint('UPSERT "%(brand)s", "%(model)s", \'%(props_hstore)s\''
                ', %(trailStr)s '% locals())
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

    
def routerWalker(curUrl):
    global prevTrail
    try:
        d = pq(url=curUrl)
        routers = d('em.router a.routerl')
        startIdx = getStartIdx()
        numRouters = len(routers)
        for idx in range(startIdx, numRouters):
            ulog('idx=%s'%idx); ulog('curUrl= '+curUrl)
            detailUrl = routers[idx].attrib['href']
            detailUrl = urlChangePath(curUrl,detailUrl)
            prevTrail+=[idx]
            scrapeDetails(detailUrl)
            prevTrail.pop()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()


def pageWalker():
    global prevTrail
    try:
        curUrl = "http://www.speedguide.net/broadband-list.php"
        startIdx = getStartIdx()
        for idx in range(0, startIdx):
            ulog('idx=%s'%idx); ulog('curUrl= '+curUrl)
            d = pq(url=curUrl)
            nextPage = d('img[alt^="Next page"]')[0]
            curUrl = nextPage.getparent().attrib['href']
            curUrl = urlChangePath(d.base_url,curUrl)

        for idx in itertools.count(startIdx):
            ulog('idx=%s'%idx); ulog('curUrl= '+curUrl)
            prevTrail+=[idx]
            routerWalker(curUrl)
            prevTrail.pop()
            d = pq(url=curUrl)
            try:
                nextPage = d('img[alt^="Next page"]')[0]
            except IndexError:
                ulog('Last page')
                break
            curUrl = nextPage.getparent().attrib['href']
            curUrl = urlChangePath(d.base_url,curUrl)
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

def main():
    global startTrail, prevTrail,conn
    try:
        startTrail = [int(re.search(r'\d+', _).group(0)) for _ in sys.argv[1:]]
        ulog('startTrail=%s'%startTrail)
        conn=sqlite3.connect('speedguide.sqlite3')
        sql("CREATE TABLE IF NOT EXISTS TFiles("
            "id INTEGER NOT NULL,"
            "brand TEXT," # "Asus"
            "model TEXT," # "RT-AC3100"
            "prod_name TEXT," # "Dual-band wireless-AC3100 gigabit router"
            "category TEXT," # "Wireless Router"
            "default_user_name TEXT,"
            "default_password TEXT,"
            "wifi_proto TEXT," # "abgn+ac"
            "availability TEXT,"
            "description TEXT,"
            "product_page TEXT,"
            "hw_fla1_amount TEXT," # '128 Mb'
            "hw_ram1_amount TEXT," # '512 Mb'
            "image_url TEXT,"
            "props_hstore TEXT," # 'a=>1,b=>"hello world",c=>True'::hstore
            "tree_trail TEXT," # [26, 2]
            "PRIMARY KEY (id),"
            "UNIQUE(brand,model)"
            ")")
        prevTrail=[]
        pageWalker()
        conn.close()
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()
        driver.save_screenshot(getScriptName()+'_'+getFuncName()+'_excep.png')


if __name__=='__main__':
    main()
