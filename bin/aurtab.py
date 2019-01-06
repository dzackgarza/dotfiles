#!/usr/bin/python
import os
import requests
import tarfile
import gzip
import sys
import subprocess

def main():
    if not os.path.exists('/usr/bin/pacman'):
        raise FileNotFoundError('Do you use Arch? Missing required pacman binary!')
    url = 'https://aur.archlinux.org/packages.gz'
    print("Pulling packages...")
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print("HTTP response error, status code %d." % r.status_code)
        sys.exit()
    print("Packages pulled.")
    gz = str(r.content).split('\\n')
    mylist = []
    for i in range(1, len(gz)-1):
        mylist.append(gz[i])
    length = len(mylist)
    print("Found {0} AUR packages.".format(len(mylist)))
    sh_mylist = []
    output = subprocess.getoutput("command pacman -Ss | grep '^[a-z]'")
    output = output.split("\n")
    print("Parsing...")
    for item in output:
        mylist.append(item.split("/")[1].split(" ")[0])
    mylist = sorted(set(mylist))
    if not os.path.exists(os.path.expanduser('~')+'/.cache/aurtab'):
        os.makedirs(os.path.expanduser('~')+'/.cache/aurtab')
    with open(os.path.expanduser('~')+'/.cache/aurtab/pkglist', 'w+') as my_file:
        for item in mylist:
            my_file.write(item+"\n")
    with gzip.open(os.path.expanduser('~')+'/.cache/aurtab/pkglist.gz', 'wb') as gout:
        my_file = open(os.path.expanduser('~')+'/.cache/aurtab/pkglist', 'rb')
        gout.writelines(my_file)
    os.remove(os.path.expanduser('~')+'/.cache/aurtab/pkglist')
    print("Completed successfully. {0} packages found; {1} AUR and {2} packages in official repositories. {3} duplicates.".format(len(mylist),length,len(output),(len(output)+length) - len(mylist)))

if __name__ == "__main__":
    main()
