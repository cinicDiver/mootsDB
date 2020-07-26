import sys
import os.path
import subprocess
import pkg_resources

def init_lib_array():
    lib_file=open(os.path.join(os.path.dirname(__file__),'./data/libs.txt'),"r")
    libs=[]
    for line in lib_file:
        line=line.strip()
        if line is not None or line != "":
            libs.append(line.strip())
    lib_file.close()
    return libs
    

def add_lib(name):
    lib_file=open(os.path.join(os.path.dirname(__file__),'./data/libs.txt'),"a")
    lib_file.write("\n")
    lib_file.write(name)
    lib_file.close()

def check_pip_install():
    try:
        import pip
    except ImportError:
        subprocess.check_call([sys.executable,"py","-3","-m","ensurepip"])


def check_lib_install():
    libs=init_lib_array()
    check_pip_install()
    lib_state={}
    for lib in libs:
        state=True
        try:
            pkg_resources.get_distribution(lib).version
        except pkg_resources.DistributionNotFound:
            state=False
        except ValueError:
            libs.remove(lib)
            continue
        lib_state[lib]=state
    return lib_state

def install_libs(lib_state):
    libs=[]
    msg=[]
    for k in lib_state.keys():
        llave=str(k).strip()
        if(lib_state[k]==False):
            libs.append(llave)
        if llave is None or llave == "":
            pass
        else:
            msg.append("{} se encuentra correctamente instalada.".format(llave))
    for lib in libs:
        try:
            subprocess.check_call([sys.executable,"python","-m","pip","install",lib])
            msg.append("{} instalada adecuadamente.".format(lib))
        except subprocess.CalledProcessError as ex:
            c=ex.returncode
            if(c==1):
                m="Subprocess returncode(1) 'not found'"
            else:
                m="Subprocess returncode(>1) 'error'"
            msg.append("{} tuvo un error de intalación: {}".format(lib,m))
    return msg