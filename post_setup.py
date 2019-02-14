import os
import urllib2


def finddirectory():
    try:
        import natlinkstatus
        status = natlinkstatus.NatlinkStatus()
        userdir = status.CoreDirectory
        if os.path.isdir(userdir):
            directory = (os.path.dirname(userdir))
            print("\nCaster: NatLink found.\n" "Defaulting to Dragon NaturallySpeaking Engine\n")
            return directory
    except Exception:
        print("\nCaster: NatLink not found.\n" "Defaulting to Windows Speech Recognition Engine\n")
        directory = os.path.join(os.environ['USERPROFILE'], "Desktop")
        if os.path.isdir(directory):
            return directory


def download():
    response = urllib2.urlopen('https://raw.githubusercontent.com/dictation-toolbox/caster/develop/_caster.py')
    html = response.read()
    directory = finddirectory()
    filename = directory + '\\_caster.py'
    f = open(filename, 'w')
    f.write(html)


def main():
    download()
    pass


if __name__ == '__main__':
    main()
