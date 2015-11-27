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


tableMD = r"""
RT-AC3100 Features  
---  
General  
Availability: |  announced   
LAN / WAN Connectivity  
WAN ports: |  1   
two USB ports for 3G/4G modems  
WAN port(s) type: |  10/100/1000 Gigabit Ethernet (RJ-45)  
WAN port auto cross-over: |  ![yes](/images/buttons/yes.gif)  
LAN ports: |  4   
LAN ports type: |  10/100/1000 Gigabit Ethernet (RJ-45)  
LAN ports auto cross-over: |  ![yes](/images/buttons/yes.gif)  
USB port(s): |  2   
one of the USB ports is USB 3.0 (for printers, storage devices and 3G/4G modems)  
USB port type: |  USB 2.0   
Router  
NAT routing: |  ![yes](/images/buttons/yes.gif)  
Multihomed: |  ![yes](/images/buttons/yes.gif)  
DMZ: |  ![yes](/images/buttons/yes.gif)  
Port forwarding: |  ![yes](/images/buttons/yes.gif)  
Port triggering: |  ![yes](/images/buttons/yes.gif)  
DHCP server: |  ![yes](/images/buttons/yes.gif)  
DHCP client: |  ![yes](/images/buttons/yes.gif)  
Dynamic DNS client: |  ![yes](/images/buttons/yes.gif)   
  
QoS: |  ![yes](/images/buttons/yes.gif)  
UPnP: |  ![yes](/images/buttons/yes.gif)  
Wireless  
Maximum Wireless Speed: |  3200 Mbps (1300ac+1300ac+600n)  
WiFi standards supported: |  802.11a (54 Mbps)  
802.11b (11 Mbps)  
802.11g (54 Mbps)  
802.11n  
802.11ac  
Wifi security/authentication: |  WEP 
WPA (TKIP)  
WPA2 (AES)  
802.1X (EAP-MD5/TLS/TTLS/PEAP)  
Wireless MAC Address filtering  
SSID Broadcast disable  
WiFi modes: |  Access point  
Wireless bridge (PtP)  
external antenna(s): |  4   
WDS compatible: |  ![yes](/images/buttons/yes.gif)  
WMM (QoS): |  ![yes](/images/buttons/yes.gif)  
WMM-PS (QoS): |  ![yes](/images/buttons/yes.gif)  
WPS (Wi-Fi Protected Setup): |  ![yes](/images/buttons/yes.gif)  
Dual Band (2.4GHz/5GHz): |  ![yes](/images/buttons/yes.gif)  
Simultaneous Dual Band (2.4GHz/5GHz): |  ![yes](/images/buttons/yes.gif)  
VPN  
| IPSec  
IPSec server: |  ![yes](/images/buttons/yes.gif)  
IPSec passthrough: |  ![yes](/images/buttons/yes.gif)  
| L2TP  
L2TP passthrough: |  ![yes](/images/buttons/yes.gif)  
| PPTP  
PPTP server: |  ![yes](/images/buttons/yes.gif)  
PPTP passthrough: |  ![yes](/images/buttons/yes.gif)  
Firewall  
DoS / DDoS protection: |  ![yes](/images/buttons/yes.gif)  
Filtering: |  Domain/URL blocking, IP Address filtering, MAC Address filtering   
Device Management  
Alternate Admin URL: |  <http://router.asus.com>  
Default admin username: |  admin   
Default admin password: |  admin   
Administration: |  Web-based (LAN)  
Quick Setup Wizard   
Firmware upgradeable: |  ![yes](/images/buttons/yes.gif)  
Configuration backup/restore: |  ![yes](/images/buttons/yes.gif)
Event log: |  ![yes](/images/buttons/yes.gif)  
Misc hardware info  
RAM: |  512 Mb   
Flash Memory: |  128 Mb   
IPv6 support: |  ![yes](/images/buttons/yes.gif)  
NTP client: |  ![yes](/images/buttons/yes.gif)  
Print Server: |  ![yes](/images/buttons/yes.gif)   
  
Links  
Product page: |  [http://www.asus.com/Networking/RT-AC3100...](http://www.asus.com/Networking/RT-AC3100/ "http://www.asus.com/Networking/RT-AC3100/" )  
Manual: |  [http://dlcdnet.asus.com/pub/ASUS/wireles...](http://dlcdnet.asus.com/pub/ASUS/wireless/RT-AC3100/E10546_RT_AC3100_Manual.pdf "http://dlcdnet.asus.com/pub/AS
US/wireless/RT-AC3100/E10546_RT_AC3100_Manual.pdf" )  
Quick Install Guide: |  [http://dlcdnet.asus.com/pub/ASUS/wireles...](http://dlcdnet.asus.com/pub/ASUS/wireless/RT-AC3100/E10547_RT_AC3100_QSG.pdf "http://dlcdnet.asus.
com/pub/ASUS/wireless/RT-AC3100/E10547_RT_AC3100_QSG.pdf" )

"""
content = """
Home  » Broadband Hardware  » List  » Asus  » RT-AC3100 Details 

|  | 

# Asus RT-AC3100  
  
---|---  
details: | Dual-band wireless-AC3100 gigabit router  
hardware type: | Wireless Router  
date added: | 2015-10-24  
updated: | 2015-11-17  
  
Whether you're gaming online in a heated competition or streaming a live event in 4K/UHD, lag and buffering are simply not an option. NitroQAM (1024-QAM) technology on the RT-AC3100 delivers a combined 3167 Mbps Wi-Fi speed, ensuring everyone on your network can enjoy smooth streaming and low-latency online gaming.   
  
The Gamers Private Network (GPN) powered by WTFast automatically performs route optimization, choosing the most efficient route for game packets, resulting in consistently-lower ping time and minimal packet loss.  
  
Boost your gaming bandwidth with Adaptive QoS (Quality of Service), which allows you to easily prioritize gaming packets and activities. You can even assign full dedicated bandwidth while gaming under gamer solo mode, making RT-AC3100 the perfect ally for low latency gaming anywhere in your home.   
  
With a four-transmit, four-receive (4T4R) antenna design, both Wi-Fi range and signal stability improve dramatically, able to reach our widest-ever coverage up to 500m2 (5400 ft). AiRadar beamforming further focuses Wi-Fi signal on your devices, making your Wi-Fi faster, clearer and stronger.  
  
Advanced parental controls help you to prevent users from visiting inappropriate websites, for example keeping young children safe from viewing adult content. You can also restrict the times that each device or guest account can access the internet, by applying scheduled time limits.   
  
With built-in USB 3.0 and USB 2.0 ports, you can connect USB-enabled devices, such as external storage drives, printers, or a 3G/4G dongle to your ASUS router and share them conveniently with other users via Wi-Fi. And with USB 3.0, you can enjoy up to 10X faster data transfer speeds.  
  


All Asus products

All Wireless Routers

  
  
» Forums search for Asus RT-AC3100  
RT-AC3100 Features  
---  
General  
Availability: |  announced   
"""

listItem = r"""
[Asus  
RT-AC3100  
Wireless Router  
](/routers/asus-rt-ac3100-dual-band-wireless-ac3100-gigabit-3603)
"""
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

def elmToMd(elm:lxml.html.Element, ignore_links=True, ignore_images=True, ignore_emphasis=True):
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
    return parse.SplitResult(sp.scheme, sp.netloc, path, sp.query, sp.fragment).geturl()


def surrDQuote(s:str)->str:
    return '"'+s+'"'

def dict2hstore(dic)->str:
    def kname(k):
        if re.match(r'\w+$', k, re.I):
            return k
        else:
            return surrDQuote(k)
    def vname(v):
        if isinstance(v, bool):
            return str(v).lower()
        elif isinstance(v, int):
            return str(v)
        elif isinstance(v,str):
            if re.match(r'\w+$',v,re.I):
                return v
            else:
                return surrDQuote(v)
        else:
            ipdb.set_trace()
    return ','.join( kname(k)+"=>"+vname(v) for k,v in dic.items())

def scrapeDetails(curUrl):
    global prevTrail
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
        j = next(j for j,_ in enumerate(mdl[i+1:]) if _.strip().startswith('details:') )
        prodName = mdl[j].split(' |' )[1].strip()
        # "Dual-band wireless-AC3100 gigabit router"
        k = next(k for k,_ in enumerate(mdl[j+1:]) if _.strip().startswith('hardware type:') )
        category = mdl[k].split(' | ')[1].strip()
        # "Wireless Router"

        # find empty line after details
        i = next(i for i,_ in enumerate(mdl[k+1:]) if not _.strip())
        # find non empty line
        j = next(j for j,_ in enumerate(mdl[i+1:]) if _.strip())
        k = next(k for k,_ in enumerate(mdl[j+1:]) if re.match(r'All \w+ products.*', _.strip()))
        prodDesc = '\n'.join(_.strip() for _ in mdl[j:k] if _.strip())
        prodPage = None

        trs = d('.tblight tr')
        pr=OrderedDict()
        for tr in trs:
            md = elmToMd(tr,False,False)
            if ' | ' not in md:
                continue
            n,v = [_.strip() for _ in l.split(' | ',1)]
            v = '\n'.join(_.strip() for _ in v.splitlines())
            assert n not in pr
            n = n.rstrip(':')
            v0 = v[0]
            if v0=='!':
                yn = re.search(r'!\[(.+?)\]', v).group(1)
                if yn=='yes': v= True
                elif yn=='no': v = False
                else: ipdb.set_trace(); uprint(yn)
            elif v0 =='<':
                v = re.search(r'<(.+?)>',v).group(1).strip()
                # "<http://router.asus.com>"
            elif v0 == '[':
                hreftitle = re.search(r'\((.+?)\)', v).group(1)
                v = hreftitle.split()[0]
            else:
                if not v0.isalnum(): ipdb.set_trace()
                if re.match(r'\d+$', v):
                    v = int(re.match(r'\d+$',v).group(0))
                else: v = v
            pr[n] = v
            if n == 'Product page':
                prodPage = v
        hstore = dict2hstore(pr)
        img= d('a.piframe img')[0]
        imgUrl=urlChangePath(d.base_url,img.attrib['src'])
        trailStr = str(prevTrail)

        sql("INSERT OR REPLACE INTO TFiles(brand,model,"
            "prod_name,category,prod_desc,image_url,product_page,props_hstore,"
            "tree_trail) VALUES (:brand,:model,:prodName,:category,:prodDesc,"
            ":imgUrl,:prodPage,:hstore,:trailStr)", locals())
        uprint('UPSERT "%(brand)s","%(model)s",\'%(hstore)s\',%(trailStr)s '%locals())
    except Exception as ex:
        ipdb.set_trace()
        traceback.print_exc()

# _56 = etree.tostring(d('em.router a.routerl')[0])
# In [66]: h.handle(_56.decode('utf-8'))
# 
# d = pq('http://www.speedguide.net/routers/asus-rt-ac3100-dual-band-wireless-ac3100-gigabit-3603')
# _85 = d('#content > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)')[0]
# _90 = parse.urlsplit('http://www.speedguide.net/routers/asus-rt-ac3100-dual-band-wireless-ac3100-gigabit-3603')
# # Out[90]: SplitResult(scheme='http', netloc='www.speedguide.net', path='/routers/asus-rt-ac3100-dual-band-wireless-ac3100-gigabit-3603', query='', fragment='')
# 
# image_url= parse.SplitResult(_90.scheme, _90.netloc, _85.attrib['src'], _90.query, _90.fragment).geturl()
# # Out[101]: SplitResult(scheme='http', netloc='www.speedguide.net', path='/img.php?x=200&img=/images/hardware/asus/rtac3100/rtac3100.jpg', query='', fragment='')
# _56 = etree.tostring(d('em.router a.routerl')[0])
    
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
            # 'http://www.speedguide.net/routers/asus-rt-ac3100-dual-band-wireless-ac3100-gigabit-3603'
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
        for idx in itertools.count(startIdx):
            ulog('idx=%s'%idx); ulog('curUrl= '+curUrl)
            prevTrail+=[idx]
            routerWalker(curUrl)
            prevTrail.pop()
            d = pq(url=curUrl)
            nextPage = d('img[alt^="Next page"]')[0]
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
            "prod_desc TEXT," # "Whether you're gaming online in a heate..."
            "image_url TEXT," # http://www.speedguide.net/img.php?x=200&img=/images/hardware/asus/rtac3100/rtac3100.jpg
            "product_page TEXT,"
            "props_hstore TEXT," # 'a=>1,b=>"hello world",c=>True'::hstore
            "tree_trail TEXT," # [26, 2]
            "PRIMARY KEY (id)"
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
