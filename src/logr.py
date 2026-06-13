import inspect


DEBUG=False

def log(msg):
    #parent_frame_info = inspect.stack()[1]
    #mod = inspect.getmodule(parent_frame_info.frame)
    #DEBUG and print(f"[DEBUG-{mod.__name__}] {msg}")
    DEBUG and print(f"[DEBUG] {msg}")
