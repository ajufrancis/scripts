#!/usr/bin/python

os = {
    'krn': 'Linux',
    'family': 'RedHat',
    'name': 'CentOS',
    'arch': 'x86_64',
    'release': '6.3',
    'kernel': 'vmlinuz',
    'initrd': 'initrd.img',
}
os['label'] = os['name'] + ' ' + os['release'] + ' ' + os['arch']

class SYSLINUX:  
    def __init__(self,os):  
        _MENU_HEADER = 'er/menuinc/header.module'
        _MENU_INC ='er/plugins/centos/5/i386/centosmain.http.menu'
        _MENU_BACK = 'er/menu/shared/menu-back.module'
        _MENU_BG = 'er/plugins/centos/centos.png'

        _MENU = '''
LABEL {name}
    MENU LABEL {name}
    KERNEL {kernel}
    INITRD {initrd}
    APPEND {append}
'''.format(name=os['label'], kernel=os['kernel'], initrd=os['initrd'], append=os['label'])

        _MENU_BOX = '''
MENU BEGIN CentOS
MENU LABEL ^{name}
# ------====> Include Menu Settings <====------
MENU INCLUDE {menu_header}
# ------====> Set Specific Page Settings <====------
MENU BACKGROUND {menu_bg}
MENU INCLUDE {menu_inc}
# ------====> Back <====------
MENU INCLUDE  {menu_back}
MENU END
'''.format(name=os['label'], menu_header=_MENU_HEADER, menu_back=_MENU_BACK, menu_bg=_MENU_BG, menu_inc=_MENU_INC)
        self.MENU = _MENU
        self.MENU_BOX = _MENU_BOX

menu = SYSLINUX(os)
print menu.MENU_BOX
