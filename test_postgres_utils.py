import postgres_utils
from postgres_utils import dict2hstore, hstore2dict
def main():
    dic = dict(Manual="http://downloads.trendnet.com/tew-828dru/manual/ug_tew-828dru(v1).pdf")
    hstore = dict2hstore(dic)
    print(hstore)

if __name__=="__main__":
    main()
