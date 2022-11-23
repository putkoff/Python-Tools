import os
import func as f
import subprocess
import stat
def delFile(x):
    makeFileCurr(os.remove(x))
def homeIt():
    slash = '\\'
    changeGlob('home',os.getcwd())
    if slash not in home:
        slash = '/'
    changeGlob('slash',slash)
def changeGlob(x,y):
    globals()[x] = y
def chmodIt(x):
    st = os.stat(x)
    os.chmod(x, st.st_mode | stat.S_IEXEC)
    os.chmod(x, 0o775)
    return 'sh '+str(x)
def pen(x,y):
    f.pen(x,makeFileCurr(y))
def reader(x):
    return f.reader(x)
def addThis(x,y,k):
    for i in range(0,k):
        x = x + y
    return x
def tabIt(x):
    cou = 1
    z = ''
    for i in range(0,len(x)):
        z = z + x[i]
        if z[-len('\n'):] == '\n':
            z = addThis(z,'\t',cou)
            cou +=1
    return z
def createPath(x,y):
    if x[-1] != slash:
        x = x + slash
    if y[0] == slash:
        y = y[1:]
    return x+y
def makeFileCurr(x):
    return createPath(os.getcwd(),x)
def createBashSamp():
    return f.exists_make(tabIt('gnome-terminal\\\n--tab\\\n--title="TAB 1" -- bash -c "export SUDO_ASKPASS='+"'"+makeFileCurr('passAsk.sh')+"';"+' ^^killme^^ &> '+makeFileCurr('output.txt')+'; $SHELL"\\'),makeFileCurr('sample_whole_sh.txt'))
def lastP(x):
    p = reader('output.txt')
    if len(p) == 0:
        return False
    if p.split('\n')[-1] == 'done':
        return 'done'
    if p.split('\n')[-1] == x:
        return False
    return True
def bash_it(x):
    ogOut = f.exists_make('',makeFileCurr('output2.txt'))
    f.pen(createBashSamp().replace('^^killme^^',x),'script.sh')
    p = os.popen(chmodIt(createPath(home,'script.sh'))).read()
    pen(ogOut+'\n'+reader('output.txt'),'output2.txt')
def createPassScript():
    pen('#!/bin/bash\nzenity --password --title=Authentication\n','passAsk.sh')
    os.popen(chmodIt('passAsk.sh'))
def sudoReplace(x):
    x = x.replace('sudo','echo -e $PASSWD | sudo -S ')
    return x
def runAllStrings(ls):
    for i in range(0,len(ls)):
        bash_it(sudoReplace(ls[i]))
def installOpenVpn():
    return ['sudo apt-get update','sudo apt-get install openvpn','sudo apt install easy-rsa -y','sudo -s','wget -O - https://swupdate.openvpn.net/repos/repo-public.gpg|apt-key add -',"echo 'deb http://build.openvpn.net/debian/openvpn/release/2.5 focal main' > /etc/apt/sources.list.d/openvpn-aptrepo.list','apt-get update && apt-get install openvpn",'exit','mkdir ~/easy-rsa','ln -s /usr/share/easy-rsa/* ~/easy-rsa/','cd ~/easy-rsa/','./easyrsa init-pki']
homeIt()
createPassScript()
