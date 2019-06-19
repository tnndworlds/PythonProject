#！/usr/bin/env python
#_*_coding:utf-8_*_

import sys
import os
from configparser import ConfigParser
from fileop import file
from tools import utils
from xsio import xml
import subprocess
import json
CFG = ConfigParser()
RootPath = utils.getProjectRootPath()

def __init():
    CFG.read(utils.getProjectRootPath() + "/cfg.ini")

def _Prepare():
    file.RMDirectory(RootPath + '/tmp')
    file.CreateDirectory(RootPath + '/tmp')
    file.DirectoryCopy(CFG.get('tools', 'wsdl2java.directory'), RootPath + '/tmp/BOOT-INF/classes/wsdl/')
    file.FileCopy(RootPath + '/resource/ServiceAgent.jar', RootPath)
    return

def _WSDLProcess():
    white_list = CFG.get('tools', 'wsdl2java.whitelist').replace('\n', '').split(',')
    cfg_list = []
    for wsdl_name in white_list:
        wsdl_file = RootPath + '/tmp/BOOT-INF/classes/wsdl/' + wsdl_name + '.wsdl'
        wsdl_obj = xml.XMLToJSON(wsdl_file)
        wsdl_obj['fileName'] = wsdl_name
        cfg_list.append(wsdl_obj)
        wsdl_cmd = CFG.get('tools', 'wsdl2java.cmd').format(wsdl_name, RootPath + '/tmp/BOOT-INF/classes/', wsdl_file)
        os.system(wsdl_cmd)
    # configuration write to /BOOT-INF/classes/wsdl2java/wsdl2java.cfg
    file.CreateDirectory(RootPath + '/tmp/BOOT-INF/classes/wsdl2java')
    output = open(RootPath + '/tmp/BOOT-INF/classes/wsdl2java/wsdl2java.cfg', 'w')
    output.write(json.dumps(cfg_list))
    output.close()

def _UpdateJAR():
    cmd = 'jar -uf ' + RootPath + '/ServiceAgent.jar' + " -C " + RootPath + "/tmp ./BOOT-INF"
    subprocess.Popen(cmd, shell=True)
    return

def main():
    print("*********Start*********")
    __init()
    ##1. copy all wsdl file to /BOOT-INF/classes/wsdl目录
    print("Stage(1/3) Prepare environment.")
    _Prepare()

    ##2. parse wsdl and execute wsdl2java command,
    print("Stage(2/3) Create server class files")
    _WSDLProcess()

    ##3. execute `jar -uf` command, update ServiceAgent.jar
    print("Stage(3/3) Generate ServiceAgent.jar")
    _UpdateJAR()

    print("*********Create ServiceAgent.jar successfully*********")
    print("*********End*********")

if __name__ == '__main__':
    main()


