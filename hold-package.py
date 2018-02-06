#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sys
import getopt
import subprocess

# default key words
hold_key = ['xorg', 'linux-image', 'linux-headers', 'hold']
# home dir
home_dir = '/home/' + os.getlogin() + '/.hold-pkg'
# package list file name
file_name = 'pkg_list'
# key words file name
key_name  = 'key_list'

# set key words
def set_key():

    global hold_key
    global key_name
    global home_dir

    if False is os.path.isdir(home_dir):
        subprocess.call('mkdir ' + home_dir, shell = True)

    file_key_list = os.path.join(home_dir, key_name)

    c = '''echo 'INFO' TO ''' + file_key_list
    ct_title = c.replace('INFO', '# hold package key words').replace('TO', '>')
    subprocess.call(ct_title, shell = True)

    str_x = ' '.join(hold_key)

    ct_msg = c.replace('INFO', str_x).replace('TO', '>>')
    subprocess.call(ct_msg, shell = True)

# get the package list by key words
# record to file_name
def get_pkg():

    global key_name
    global file_name
    global home_dir
    key_list = []

    file_key_list = os.path.join(home_dir, key_name)
    if False is os.path.isfile(file_key_list):
        print('please run \' hold-package --init \' first!')
        return False
    else:
        with open(file_key_list, 'r') as f:
            for l in f.readlines():
                if '#' is l.strip()[0]:
                    pass
                else:
                    for x in l.strip().split(' '):
                        x = re.sub('[\r\n\t]', '', x)
                        if True is any(x):
                            key_list.append(x)

        f_name = os.path.join(home_dir, file_name)
        subprocess.call('''echo '# well be hold package list and status' > ''' + f_name, shell = True)
        get_pkg_order = 'dpkg --get-selections | grep '
        for s in key_list:
            subprocess.call(get_pkg_order + s + ' >> ' + f_name, shell = True)

# print list
def show_pkg(str_c):

    global home_dir
    global key_name
    global file_name

    f_tmp = '''/tmp/12107030.tmp'''
    get_pkg_order = 'dpkg --get-selections | grep '
    subprocess.call('rm ' + f_tmp + ' -rf ', shell = True )

    for x in str_c.split(' '):
        if x == 'list':
            f_name = os.path.join(home_dir, file_name)
            with open(f_name, 'r') as f:
                for l in f.readlines():
                    print(l[:-1])
        elif x == 'key':
            f_name = os.path.join(home_dir, key_name)
            with open(f_name, 'r') as f:
                for l in f.readlines():
                    print(l[:-1])
        else:
            subprocess.call(get_pkg_order + x + ' >> ' + f_tmp, shell = True )

    if os.path.isfile(f_tmp):
        with open(f_tmp, 'r') as f:
            for l in f.readlines():
                print(l[:-1])

# hold or install package
def handle_pkg(str_c):

    global home_dir
    global file_name

    f = os.path.join(home_dir, file_name)
    if False is os.path.isfile(f):
        print('error, package list false !')
        print('please run \' hold-package --init  \' first!')
    else:
        with open(f, 'r') as fr:
            for l in fr.readlines():
                if '#' not in l:
                    c = l.split('\t')[0]
                    c = str_c.replace('PNAME', c)
                    print(c)
                    subprocess.call(c, shell = True)

def hold_pkg():
    handle_pkg('''echo "PNAME hold" | dpkg --set-selections''')

def unhold_pkg():
    handle_pkg('''echo "PNAME install" | dpkg --set-selections''')


str_help = '''
--help      查看帮助;
--init      写默认关键字到key_list,按照关键字查找包并写入pkg_list;
            文件在~/.hold-pkg目录下,可以手动改写,使用'#'注释,只支持整行注释;
--list      按照key_list表刷新pkg_list;
--hold      按照pkg_list列表名称hold package;
--unhold    按照pkg_list列表名称解除package的hold状态;
--show      按参数的关键字查看包状态;
            --show list, 查看按照关键字找到的包列表
            --show key,  查看关键字列表
            --show 'nvidia xorg', 查看包含关键字‘nvidia’或‘xorg’的包的状态
'''
# main entry
if __name__ == '__main__':
    # check param
    if 1 == len(sys.argv):
        print(str_help)
        sys.exit(0)
    try:
        options,args = getopt.getopt(sys.argv[1:], "123456:", ["help", "init", "list", "hold", "unhold", "show="])
        for name, value in options:
            if name in ('--help'):
                print(str_help)
            elif name in ('--init'):
                set_key()
                get_pkg()
            elif name in ('--list'):
                get_pkg()
            elif name in ('--hold'):
                hold_pkg()
            elif name in ('--unhold'):
                unhold_pkg()
            elif name in ('--show'):
                show_pkg(value)
    except getopt.GetoptError:
        print('input param error, check pls!')
