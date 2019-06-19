#! /usr/bin/env pythong
#_*_coding:utf-8_*_

import os
import shutil

def CreateDirectory(directory):
    print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return

def ClearDirectory(directory):
    if not os.path.exists(directory):
        return
    ls = os.listdir(directory)
    for i in ls:
        del_path = os.path.join(directory, i)
        if os.path.isfile(del_path):
            os.remove(del_path)
        else:
            ClearDirectory(del_path)
    return

def RMDirectory(directory):
    if not os.path.exists(directory):
        return
    shutil.rmtree(directory)
    return

def DirectoryCopy(srcDir, desDir):
    if not os.path.exists(srcDir):
        print("Source directory not exist.")
        return
    CreateDirectory(desDir)
    ClearDirectory(desDir)
    for root, dirs, files in os.walk(srcDir):
        for file in files:
            srcFile = os.path.join(root, file)
            shutil.copy(srcFile, desDir)
    return

def FileCopy(srcFile, desDir):
    CreateDirectory(desDir)
    shutil.copy(srcFile, desDir)