import os

for root, dir, file in os.walk('./'):
    for i in file:
        if i.endswith('ui'):
            path = os.path.join(root,i)
            py_path = f'./ui/{i.split(".")[0]}.py'
            print(f'pyuic5 {path} -o {py_path}')
            os.popen(f'pyuic5 {path} -o {py_path}')
