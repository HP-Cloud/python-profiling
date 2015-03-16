from types import FunctionType, MethodType
from importlib import import_module
import pkgutil
import time

f = file('output.txt', 'w')

def aop(func):
    def wrapper(*args, **kwds):
        fn_name = func.__module__ + "." + func.__name__
        print "==========================="
        print "before call"
        print >>f,  fn_name + " start"
        start = time.clock()
        print func
        value = func(*args, **kwds)
        print "after call"
        end = time.clock()
        print >>f,  fn_name + " end"
        print >>f,fn_name + ": " + str(end-start) + "s"
        print fn_name + ": " + str(end-start) + "s"
        print "==========================="
        return value
    return wrapper

def makePath(list):
    str=''
    for s in list:
        if s:
            str =s+ '.'+str
    str=str[:-1]
    return str

def aopp(pkname,ppkname):
    package = makePath([pkname,ppkname])
    print package
    module = import_module(package)
    for _, name, ispk in pkgutil.iter_modules(module.__path__):
        print name,ispk
        if name == 'conf':
            continue
        if ispk:
            print package,name
            aopp(name,package)
        else:
            module_name = makePath([name,package])
            print module_name
            m = import_module(module_name)
            for attr in dir(m):
                item = getattr(m, attr)
                if type(item) in [FunctionType,MethodType]:
                    print '-----------'
                    setattr(m,attr, aop(item))


aopp('neo','')
aopp('neolib','')
aopp('neoapp','')
