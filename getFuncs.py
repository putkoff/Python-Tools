import json
import os.path
import shutil
import json
from web3 import Web3
import os
import time
import stat
import subprocess
#HomeFunctions---------------------------------------------------------------------------------------------------------------------------------------------------------------
def removeFromList(x,y):
    i = findIt(x,y)
    if i == len(y):
        return y[:-1]
    ls = []
    for i in range(0,len(y)):
        if y[i] != x:
            ls.append(y[i])
    return ls
def openFileExplorer(x):
    x ='open '+x
    subprocess.Popen(x, shell=True)
def allSizeDays(x,ls,i):
    return timeSpacing(ls,i,str(calcTimeInDays(foldTime(x,ls,i))),str(calcKb(foldSize(x,ls,i))))
def getFolder(x):
    exit = False
    n = x
    avoid = True
    #avoid = boolAsk("avoid hidden?")
    while exit != True:
        foldList = os.listdir(x)
        if avoid == True:
            foldList = removeFromList(foldList,'.',0)
        ask = create_ask(foldList,'which file would you like to use?')
        if ask == "exit":
            exit == True
        elif ask == "back":
            n = buildToSplitLast(n,slash)
        elif  ask == "open":
            openFileExplorer(x)
        elif str(ask) in foldList:
            n = n+slash+ask
        else:
            n = n+slash+ask
        if isFold(n) == True:
            if boolAsk(fileInputString(splitTo(n,slash,-1))) == False:
                n = buildToSplitLast(n,slash)
            else:
                return n
        x = n+slash        
#ASKfunctions-----------------------------------------------------------------------------
def create_ask(x,y):
        alph = get_alph()
        n = y + '\n0) to exit\n1) back\n2) openFileExplorer\n3) enter filePath\n\n'
        alph = createAlph(len(x))
        alphGood = ['0','1','2','3']
        for i in range(0,len(x)):
        	alphGood.append(alph[i])
        	n = n + str(alph[i]) + ') '+str(x[i])+'\n'
        while True:
        	ask = input(n)
        	if ask in alphGood:
        		if ask == str(0):
        		    return True
        		if ask == str(1):
        		    return "back"
        		if ask == str(2):
        		    return "open"
        		if ask == str(3):
        		    return "custom"
        		i = find_it_alph(alph,str(ask))
        		return x[i]
        	print('looks like you entered an input that was not selectable,please re-input your selection')
def lowerList(x):
    lsN = []
    if isLs(x) == False:
        x = [x]
    for i in range(0,len(x)):
        lsN.append(str(x[i]).lower())
    return lsN
def boolAsk(x):
    yes = ['y','yes','true','t','','0']
    no = ['n','no','false','f',1]
    ask = input(x+'\n0) yes\n1) no\n')
    ask = str(ask).lower()
    if ask.lower() in lowerList(yes):
        return True
    return False
def AnyAsk(x):
    if len(x) == 2:
        inp = x[0]+'\n0) exit\n'+x[1]
    else:
        inp = x+'\n0) exit\n'
    ask = input(inp)
    if ask == '0':
        return 'exit'
    return ask
#CleanStrings--------------------------------------------------------------------------------------------------------------------------------------------
def isFile(x):
    return os.path.isfile(x)
def buildToSplitLast(x,y):
    nSpl = splitIt(x,y)
    n = ''
    if nSpl != False:
        for i in range(0,len(nSpl)-1):
            n += nSpl[i] + y
        return removeLast(n,y)
    return x
def removeFromList(x,y,i):
    newLs = []
    if i == int(-1):
        for l in range(0,len(x)):
            if y not in x[l]:
                newLs.append(x[l])
    else:
        for l in range(0,len(x)):
            if y != x[l][i]:
                newLs.append(x[l])
    return newLs

def fileInputString(x):
    return "is "+str(x)+" the file you would like to choose?"

def splitTo(x,spl,i):
    tryIt = x
    num = splitNum(x,spl)
    keepUp = True
    while keepUp == True:
        if i == -1 and num == 1:
            return x
        tryIt = x.split(spl)[i]
        if num > i:
            if fileInputString(tryIt) != False:
                return tryIt
            
            i +=1
def find_it_alph(x,k):
    i = 0
    print(x)
    while str(x[i]) != str(k):
        i = i + 1
    return i
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def findIt(x,ls):
    for i in range(0,len(ls)):
        if x == ls[i]:
            return i
    return None
def findIt(x,y):
    for i in range(0,len(y)):
        if y[i] == x:
            return i
    return False
def calcTimeInDays(x):
    return str(round((getTime()-x)/(60*24*60),2))+' days'
def calcKb(x):
    return str(round(x/1000,2))+' kb'
def foldTime(x,ls,i):
    return os.stat(x+'/'+ls[i])[9]
def foldSize(x,ls,i):
    return os.stat(x+'/'+ls[i])[6]
def timeSpacing(x,i,time,size):
    teb = ' \t'
    h = x[i]
    var = [time,size]
    teb = '             '
    exSpace = len(str()+teb)-len(str(x[i]))
    for k in range(0,2):
        te = ' \t'
        if k ==0:
            te = ' \t'
            now = exSpace-(len(x)+len(te))
            take = int(now)/len(' ')
            for c in range(0,int(exSpace)):
                h = h+' '
        h = h+te+var[k]
    return  h
def createAlph(i):
    k = int(i/int(26) + 1)
    alph = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
    alphNew = []
    alLen = i
    for l in range(0,k):
        lenNow = i
        if i>int(26):
            lenNow = int(26)
        for c in range(0,lenNow):
            n = alph[c]
            for ck in range(0,l):
                n = n + alph[c]
            alphNew.append(n)
        i -=1
    return alphNew
def get_alph():
    alph = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg,hh,ii,jj,kk,ll,mm,nn,oo,pp,qq,rr,ss,tt,uu,vv,ww,xx,yy,zz,aaa,bbb,ccc,ddd,eee,fff,ggg,hhh,iii,jjj,kkk,lll,mmm,nnn,ooo,ppp,qqq,rrr,sss,ttt,uuu,vvv,www,xxx,yyy,zzz,aaaa,bbbb,cccc,dddd,eee,fff,ggg,hhh,iii,jjj,kkk,lll,mmm,nnn,ooo,ppp,qqq,rrr,sss,ttt,uuu,vvv,www,xxx,yyy,zzz'
    return alph.split(',')
def isFold(x):
    return os.path.isdir(x)
def splitIt(x,y):
    if str(y) in str(x):
        return x.split(y)
    return False
def removeLast(x,y):
    if x.replace(x[0:-len(y)],'') == y:
        return x[0:-len(y)]
    return x
def splitNum(x,spl):
    return len(x.split(spl))
def getTime():
    return time.time()
def reader(file):
    with open(file, 'r') as f:
        text = f.read()
        return text
def pen(paper, place):
    with open(place, 'w') as f:
        f.write(str(paper))
        f.close()
def get_curr_path():
    return os.getcwd()
def listFiles(x):
    return os.listdir(x)
def homeIt():
    curr = get_curr_path()
    slash = '//'
    if '//' not in str(curr):
        slash = '/'
    changeGlob('slash',slash)
    changeGlob('home',curr)
    return curr,slash
def changeGlob(x,v):
    globals()[x] = v
def ifOverZero(x):
    if len(x) >1:
        return True
    return False
def strInList(x,ls):
    if ifOverZero(x) == True:
        if x[0] in ls:
            return x[1:]
    return False
def eatInnerMod(x,ls):
    if strInList(x,ls) != False:
        x = strInList(x,ls)
    return x
def strInListRev(x,ls):
    if ifOverZero(x) == True:
        if x[-1] in ls:
            return x[:-1]
    return False
def eatOuterMod(x,ls):
    if strInListRev(x,ls) != False:
        x = strInListRev(x,ls)
    return x
def createPath(x,y):
    x = eatOuterMod(x,[slash,' ',''])
    y = eatInnerMod(y,[slash,' ',''])
    return x+slash+y
def eatAllMod(x,ls):
    return eatInnerMod(eatOuterMod(x,ls),ls)
def limitList(ls,ls2):
    lsN = []
    for i in range(0,len(ls2)):
        if ls2[i] not in ls:
            lsN.append(ls2[i])
    return lsN
def splitDef(x):
    return x.split('def ')
def getNeeds(x,ls):
    lsN = []
    x = splitDef(reader(x))
    for k in range(1,len(x)):
        m = x[k]
        spl = m.split(' ')
        for c in range(0,len(spl)):
            if '(' in spl[c]:
                new = spl[c].split('(')[:-1]
                for j in range(0,len(new)):
                    if new[j] not in ['split','str','range','len','input','print'] and ')' not in new[j] and '[' not in new[j]:
                        if '+' in new[j]:
                            new[j] = new[j].split('+')[-1]
                        if ',' in new[j]:
                            new[j] = new[j].split(',')[-1]
                        if '=' in new[j]:
                            new[j] = new[j].split('=')[-1]
                        if ' ' in new[j]:
                            new[j] = new[j].split(' ')[-1]
                        if ':' in new[j]:
                            new[j] = new[j].split(':')[-1]
                        if '.' not in new[j] and new[j] not in ['split','str','range','len','input','print','int'] and new[j] not in ls and new[j] not in lsN:
                            lsN.append(new[j])
    return lsN
def getCalls(x,ls):
    lsN = []
    x = reader(x)
    imps = x.split('def ')[0]
    x = x.replace(imps,'').split('\n')
    for i in range(0,len(x)):
        if len(x[i]) !=0:
            if x[i][:len('\t')] != '\t' and x[i][:len('def ')] != 'def ' and x[i][0] != ' ':
                if '(' in x[i]:
                    new = x[i].split('(')[:-1]
                    for j in range(0,len(new)):
                        if new[j] not in ['split','str','range','len','input','print'] and ')' not in new[j] and '[' not in new[j]:
                            if '+' in new[j]:
                                new[j] = new[j].split('+')[-1]
                            if ',' in new[j]:
                                new[j] = new[j].split(',')[-1]
                            if '=' in new[j]:
                                new[j] = new[j].split('=')[-1]
                            if ' ' in new[j]:
                                new[j] = new[j].split(' ')[-1]
                            if ':' in new[j]:
                                new[j] = new[j].split(':')[-1]
                            if '.' not in new[j] and new[j] not in ['split','str','range','len','input','print','int'] and new[j] not in ls and new[j] not in lsN:
                                lsN.append(new[j])
    return lsN
def isTypeFile(x,path,ls):
    lsN,lsN2 = [],[]
    for i in range(0,len(ls)):
        if isFile(createPath(path,ls[i])):
            if x in ls[i]:
                lsN.append(ls[i])
        if isFold(createPath(path,ls[i])):
            lsN2.append(ls[i])
    for i in range(0,len(lsN)):
        lsN2.append(lsN[i])
    return lsN2
def fileAsk():
    while True:
        file = str(AnyAsk(['please enter a file path','enter here: ']))
        if file == 'exit':
            return file
        print(file,file.split(slash)[-1],isFile(file))
        if isFile(file) == True:
            if '.py' not in file.split(slash)[-1]:
                if boolAsk('looks as if the file '+str(x.split(slash)[-1])+' is not a python file, did you want to continue anyway?'):
                    return file
            else:
                return file
        else:
            print('looks like that is not a recognized file')
def displayFiles(x):
    exit = False
    n = x
    avoid = True
    #avoid = boolAsk("avoid hidden?")
    while exit != True:
        x = x.split(' ')[0]
        foldList = os.listdir(x)
        if avoid == True:
            foldList = isTypeFile('.py',x,removeFromList(foldList,'.',0))
            
            ls = []
            lsGet = []
            for i in range(0,len(foldList)):
                ls.append(allSizeDays(x,foldList,i))
                lsGet.append(x)
        ask = create_ask(ls,'current Directory '+str(x)+'\nwhich file would you like to use?')
        ask = str(ask.split(' ')[0])
        if ask == "exit":
            exit == True
        elif ask == "back":
        	n = buildToSplitLast(n,slash)
        elif  ask == "open":
               openFileExplorer(x)
        elif  ask == "old":
            return getFolder(x)
        elif ask == "custom":
            n = str(fileAsk())
            if x == 'exit':
                return 'exit'
        elif str(ask) in foldList:
            n = n+slash+ask
        else:
            n = n+slash+ask
        if isFile(n) == True:
            if boolAsk(fileInputString(splitTo(n,slash,-1))) == False:
            	n = buildToSplitLast(n,slash)
            else:
                return x,n
        x = n+slash


def getHaves(x):
    lsN = []
    x = splitDef(reader(x))
    for i in range(0,len(x)):
        n = eatAllMod(x[i],[' ','','\n','\t','\\','+'])
        lines = n.split('\n')
        if len(lines[0])!= 0:
            if lines[0][0] != '#':
                lsN.append(lines[0].split('(')[0])
    return lsN
def getAllNeeds(x):
    have = getHaves(x)
    return getNeeds(x,have)+getCalls(x,have)
def isLs(x):
    if type(x) is list:
        return True
    return False
def getDest(last):
    lsOld = []
    print('picking the current file to analyze')
    last,dep = displayFiles(last)
    while True:
        print('picking the old file to locate functioins from')
        last,old = displayFiles(last)
        lsOld.append(old)
        if boolAsk('are you done, you can choose another file to scan on top of this one?'):
            return [dep,lsOld]
def createFunSheet(x,lsNeed):
    if isLs(x) != True:
        x = [x]
    lsDef = []
    for i in range(0,len(x)):
        spl = splitDef(reader(x[i]))
        for k in range(0,len(spl)):
            lsDef.append(spl[k])
    x = lsDef
    penIt = x[0]
    lsN = []
    pen('','temp.py')
    OgNeed = lsN
    while len(lsNeed) != 0:
        for i in range(1,len(x)):
            if x[i].split('\n')[0].split('(')[0] in lsNeed and x[i] not in lsN:
                penIt = penIt +'def '+x[i] 
                lsN.append(x[i])
        pen(penIt,'temp.py')
        lsNeed = getAllNeeds('temp.py')
        if OgNeed == lsNeed:
            lsNeed = []
        OgNeed = lsNeed
    pen(penIt,'functionsNew.py')
    print('functions sheet created: as functionsNew.py located at '+str(home))
    return lsN
homeIt()
last = home
dep,lsOld = getDest(home)
createFunSheet(lsOld,getAllNeeds(dep))


