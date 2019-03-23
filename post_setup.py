import os
import urllib2

def finddirectory():
    try:
        import natlinkstatus
        status = natlinkstatus.NatlinkStatus()
        coredir = status.CoreDirectory
        directory = (os.path.dirname(coredir))
        print("\nCaster: NatLink found.\n" "Defaulting to Dragon NaturallySpeaking Engine\n"
              "Caster will automatically start with Dragon NaturallySpeaking\n")
        return directory  # NatLink MacroSystem Directory
    except Exception:
        directory = os.path.join(os.environ['USERPROFILE'], "Desktop")
        print("\nCaster: NatLink not found.\n" "Defaulting to Windows Speech Recognition Engine\n"
              "Click on '_caster' on desktop to launch WSR with Caster\n")
        return directory  # Windows User Desktop Directory


def download():
    try:
        url = 'https://raw.githubusercontent.com/dictation-toolbox/caster/develop/_caster.py'
        response = urllib2.urlopen(url, timeout=10)
        html = response.read()
        directory = finddirectory()
        filename = os.path.join(directory, '_caster.py')
        with open(filename, 'w') as f:
            f.write(html)
    except TypeError as e:
        print ('TypeError = ' + str(e))
    except IOError as e:
        print ('IOError = ' + str(e))
    except urllib2.HTTPError, e:
        print ('HTTPError = ' + str(e.code))
    except Exception:
        import traceback
        print ('Generic Exception: ' + traceback.format_exc() + "\nCaster: Report Error to "
                                                                "https://github.com/dictation-toolbox/caster/issues\n")


def main():
    download()
    pass


if __name__ == '__main__':
    main()
