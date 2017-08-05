# check if running in a jupyter notebook
try:
    shell = get_ipython().__class__.__name__
    if shell != "ZMQInteractiveShell":
        raise Exception(shell)
except:
    raise
