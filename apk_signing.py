#!/usr/bin/env python
# coding=utf-8

# How to use this script: 
# $ python android-signing.py unsigned_package.apk keystore_to_use('france' or 'bilbao')

import csv
import os
import commands
import sys
import subprocess as sp

print '########################################################################################'
print '#                                                                                      #'
print '# How to use this script:                                                              #'
print '# Think of changing the root to ./zipalign                                             #'
print '# python android-signing.py unsigned_package.apk keystore_to_use("france" or "bilbao") #'
print '#                                                                                      #'
print '########################################################################################'

# Arguments of the script
unsigned_package = sys.argv[1]
signed_package = unsigned_package[9:]
keystore_type = sys.argv[2]

temp_name = 'temp_package.apk'

if keystore_type == 'france':
    # Declaration of keystore variables for baturamobilefrance
    keystore = 'baturamobilefrance.keystore'
    keystore_storepass = 'baturamobilefrance606'
    keystore_dir = ""
    keystore_alias = 'baturamobilefrance'

if keystore_type == 'bilbao':
    # Declaration of keystore variables for baturamobilesolutions
    keystore = 'baturamobilesolutions.keystore'
    keystore_storepass = 'baturamobilesolutions606'
    keystore_dir = ""
    keystore_alias = 'baturamobilesolutions'

# Verifying that a keystore has been defined
if 'keystore' not in locals():
    print '- keystore was not defined.'
    sys.exit(0)

# Executing jarsigner
print '- Executing jarsigner...'
os.system("jarsigner -storepass "+keystore_storepass+" -keystore "+keystore+" -signedjar "+temp_name+" "+unsigned_package+" "+keystore_alias)

# Testing signed package
p = sp.Popen(['jarsigner','-verify',temp_name], stdout=sp.PIPE)
result = p.communicate()[0]

if result != 'jar verified.\n':
    print '- jarsigner failed.'
    sys.exit(0)
else:
    print '- Package correctly signed.'

# Aligning the package
print '- Aligning the package...'
os.system('/Library/android-sdk-mac_86/tools/./zipalign -f 4 '+temp_name+' '+signed_package)

# Testing aligned package
p = sp.Popen(['/Library/android-sdk-mac_86/tools/./zipalign','-c','-v','4',signed_package], stdout=sp.PIPE)
result = p.communicate()[0]

if 'FAILED' in result:
    print '- zipalign failed.'
    sys.exit(0)
else:
    print '- Package correctly aligned.'

# Removing temp file
os.remove(temp_name)
os.remove(unsigned_package)

# Everything's allright
print '- Package ' + unsigned_package + ' was correctly signed and aligned into ' + signed_package