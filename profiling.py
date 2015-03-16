from types import FunctionType, MethodType
from importlib import import_module
import pkgutil
import time


f = file('output.txt', 'w')



def aop(func):
    def wrapper(*args, **kwds):
        fn_name = func.__module__ + "." + func.__name__
        start = time.clock()
        value = func(*args, **kwds)
        end = time.clock()
        print >>f,fn_name + " cost time: " + str(end-start) + "s"
        return value
    return wrapper


def makePath(list):
    # remove empyt item
    list = filter(bool, list)
    return '.'.join(list)


def profiling(package, parent_package):
    pkpath = makePath([package, parent_package])
    modules = import_module(pkpath)

    for _, pkname, ispk in pkgutil.iter_modules(modules.__path__):
        # skip conf package
        if pkname == 'conf':
            continue
        if ispk:
            profiling(pkpath, pkname)
        else:
            mpath = makePath([pkpath, pkname])
            print mpath
            module = import_module(mpath)
            for name in dir(module):
                attr = getattr(module, name)
                print attr
                print type(attr)
                if type(attr) in [FunctionType, MethodType]:
                    print '--------------in -------------'
                    setattr(module, name, aop(attr))


profiling('neo', '')
profiling('neolib', '')
profiling('neoapp', '')

