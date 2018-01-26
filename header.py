#/usr/bin/env python3
import os
import sys

HEADER = """/* 
 * This application was developed by Aktiun, Inc. for PayPal.  
 * Unauthorized sharing and/or distribution of this file to  
 * third parties, via any medium is strictly prohibited.
 * 
 * This data application uses the ChartFactor toolkit.  Its 
 * licence document can be found in the root folder of the 
 * source code of this data application.
 * 
 * Written by Aktiun Inc.  Proprietary and confidential.
 * Copyright (C) Aktiun, Inc - All Rights Reserved
 */"""

OLD_HEADER = """/* 
 * This application was developed by Aktiun, Inc. for PayPal.  
 * Unauthorized sharing and/or distribution of this file to  
 * third parties, via any medium is strictly prohibited.
 * Proprietary and confidential.
 * Written by Aktiun Inc.  For more information, visit aktiun.com.
 * Copyright (C) Aktiun, Inc - All Rights Reserved
 */"""

EXCLUDED = ["node_modules",".json",".git","zoomdata-client.min","CFToolkit-"]
EXTENSIONS = [".js",".css"]


def excludeFile(filepath):
    for excl in EXCLUDED:
        if excl in filepath:
            return True
    return False

def main(path_to_search):
    files_list = []
    for dirpath, dirnames, filenames in os.walk(path_to_search):
        for filename in filenames:
            fullFile = os.path.join(dirpath, filename)
            for ext in EXTENSIONS:
                if ext in filename and not excludeFile(fullFile):
                    files_list.append(fullFile)

    print("Including in files")
    for fi in files_list:
        with open(fi, "r+") as f:
            text = f.read()
            fileHeader = HEADER + "\n"
            if OLD_HEADER in text:
                print(fi)
                text = text.replace(OLD_HEADER, fileHeader)
                f.seek(0)
                f.write(text)
                f.truncate()
            elif HEADER not in text:
                print(fi)
                f.seek(0)
                f.write(fileHeader + text)
                f.truncate()


if __name__ == '__main__':
    path = "."
    args = sys.argv
    if len(args) > 1:
        path = args[1]
    main(path)


