import os
import sys
current_dir = os.getcwd()
print("current dir", current_dir)
#sys.path.append(current_dir)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
print("parent dir", parent_dir)
sys.path.append(parent_dir)



# REFERENCE to root dir ("zz_PROYECTOS_geype")
parent_parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir)) # ../dir_A
print("parent parent dir", parent_parent_dir)
sys.path.append(parent_parent_dir)

'''
def add_referencia(dir_name):
	parsers_path = os.path.abspath(os.path.join(parent_parent_dir, dir_name)) # ../dir_A
	sys.path.append(parsers_path)

# REFERENCE to parsers dir
#parsers_dir = "parsers"
add_referencia("parsers")
add_referencia("splitters")
add_referencia("text_file")

print("path ", sys.path)


# REFERENCE to parsers dir
parsers_dir = "parsers"
parsers_path = os.path.abspath(os.path.join(parent_parent_dir, parsers_dir)) # ../dir_A
sys.path.append(parsers_path)

print("path ", sys.path)
'''