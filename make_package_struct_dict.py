

import re
import os

package_path = cwd = '/Users/baylieslab/Documents/Amelia/code_dev/projects/bob_py/bob_idk/bob_py'

# files_to_use = ['exper.py', 'hseg.py', 'cell.py', 'nuc.py']
files_to_use = ['exper.py', 'hseg.py', 'cell.py']

# groups_to_exclude = ['to_string functions']
groups_to_exclude = ['to_string functions', 'dev', 'general']


class_name_pat = re.compile('class (\w*) \:')
func_group_pat = re.compile('# \{ <([^>\/]*)>(.*)# \} (<\/\\1>)',flags=re.DOTALL)
func_args_pat = re.compile('\n\s*def (\w*)\(([^\)]*)\)')

package_dict = {}

for file_name in files_to_use :
    file_path = os.path.join(package_path, file_name)
    with open(file_path, 'r') as f :
        raw_text = f.read()


    class_name_match = class_name_pat.search(raw_text)
    class_name = class_name_match.group(1)

    package_dict[class_name] = {}
    func_group_match = func_group_pat.findall(raw_text)

    for val in func_group_match :

        group_name = val[0]
        # print(group_name)
        if group_name in groups_to_exclude :
            continue

        group_raw_text = val[1]

        func_list = []

        func_args_match = func_args_pat.findall(group_raw_text)
        for func_args in func_args_match :
            # func_args = list(func_args  )
            # func_name = func_args.pop(0)
            func_name = func_args[0]
            func_arg_str = func_args[1]

            # print(func_args)
            # if func_args[0] == "self" :
            #     func_args = func_args[1:]
            # print(func_args)


            func_arg_str = func_arg_str.replace('self, ','')
            func_arg_str = func_arg_str.replace('self','')
            new_func_str = '{}({})'.format(func_name, func_arg_str)

            func_list.append(new_func_str)

        package_dict[class_name][group_name] = func_list

with open('butts.py', 'w') as f :
    f.write('bob_package_dict = ')
    f.write(str(package_dict))
