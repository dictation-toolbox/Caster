import random


from caster.lib import settings
from caster.lib.dfplus.state.actions2 import BoxAction
from caster.lib.pita import scanner
from caster.lib.pita.selector import get_similar_symbol_name


def receive_pronunciation(data, nexus):
    '''get pronunciation'''
    pronunciation=data[0].split("\n")[0]
    if pronunciation=="" or pronunciation.isspace():
        return
    
    '''get other symbols in file'''
    directory_index = int(data[1][1])
    file_index = int(data[1][2])
    chosen_directory = scanner.DATA["directories"].keys()[directory_index]
    chosen_file = scanner.DATA["directories"][chosen_directory].keys()[file_index]
    names = scanner.DATA["directories"][chosen_directory][chosen_file]["names"]
    
    '''get symbol'''
    symbol = data[1][0].split(settings.HMC_SEPARATOR)[-1]
    
    '''get algorithm guesses for file'''
    ten_guesses = get_similar_symbol_name(pronunciation, names)
    
    '''write to file'''
    entry = [pronunciation, symbol]+[x for x in ten_guesses if x!=symbol]
    log_file_path = settings.SETTINGS["paths"]["PITA_LOG_FOLDER"] + "/pita_matches.log"
    with open(log_file_path, "a") as log_file:
        log_file.write(str(entry) + "\n")
    
    '''relaunch'''
    trainer_box(nexus)


def trainer_box(nexus):
    data = scanner.DATA
    '''pick a random symbol from the scanned directory'''
    directories = data["directories"].keys()
    directory_count = len(directories)
    if directory_count == 0:
        print("Must scan directory before training.")
        return
    
    names = None
    directory_index = None
    file_index = None
    while names is None:
        directory_index= random.randint(0, directory_count - 1)
        chosen_directory = directories[directory_index]
        files = data["directories"][chosen_directory].keys()
        files_count = len(files)
        if files_count == 0:
            continue 
        file_index = random.randint(0, files_count - 1)
        chosen_file = files[file_index]
        _names = data["directories"][chosen_directory][chosen_file]["names"]
        if len(_names) > 0:
            names = _names
    symbol = names[random.randint(0, len(names) - 1)]
    
    try: # make sure that the box action doesn't still exist
        data = nexus.comm.get_com("hmc").kill()
    except Exception:
        pass
    
    BoxAction(lambda _data: receive_pronunciation(_data, nexus), 
          rdescript="Train Symbol Data",
          box_settings={"instructions": "Please Pronounce: " + symbol,
                        "directory": str(directory_index),
                        "file": str(file_index) },
          box_type=settings.QTYPE_INSTRUCTIONS).execute()
    

    
    
    
