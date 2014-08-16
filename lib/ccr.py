from lib import paths, settings, utilities
import io, sys
from dragonfly import Text

def change_CCR(enable_disable, ccr_mode):
    enable = True if str(enable_disable) == "enable" else False
    ccrm = str(ccr_mode)
    
    # Make the combined file
    compatibility_success = combine_CCR_files(enable, ccrm)
    if  not compatibility_success[0]:
        utilities.report(compatibility_success[1])
        return
    
    
    
    
    print enable_disable + " ... " + ccr_mode



def combine_CCR_files(enable, a, b="", c="", d=""):
    # enable is a Boolean
    # a,b,c,d are all the same dynamically generated choice, some may be blank-- that should be determined here
#     utilities.remote_debug()
    try:
        str_a = str(a)
        str_b = str(b)
        str_c = str(c)
        str_d = str(d)
        chosen_modes = []
        for s in [str_a, str_b, str_c, str_d]:
            if not s == "":
                chosen_modes.append(s)
        
        config_settings = settings.get_settings()  # this is a dictionary of settings.json
        backup = []
        def reset_settings():
            for setting in config_settings:
                if setting in backup:
                    config_settings[setting] = True
        
        if enable:
            # in case there is a compatibility problem, save what was active before changing the settings
            for s in config_settings:
                if config_settings[s] == True:
                    backup.append(s)
            # now change the settings 
            for cm in chosen_modes:
                config_settings[cm] = True
        else:
            for cm in chosen_modes:
                config_settings[cm] = False

        # now, using the settings, scan in all the appropriate files and check for compatibility
        relevant_configs = {}
        relevant_configs["non_cmd"] = []
        relevant_configs["mapping"] = []
        relevant_configs["extras"] = []
        relevant_configs["defaults"] = []
        for m in config_settings:
            if config_settings[m] == True:
                with open(paths.get_generic_config_path() + "\\config" + m + ".txt", "r") as f:
                    # these three Booleans will determine where a line gets put in the big dictionary
                    mapping = False
                    extras = False
                    defaults = False
                    lines = f.readlines()
                    for line in lines:
                        no_whitespace = line.strip()
                        
                        if line.startswith("cmd.map"):
                            mapping = True
                            continue
                        elif line.startswith("cmd.extras"):
                            extras = True
                            continue
                        elif line.startswith("cmd.defaults"):
                            defaults = True
                            continue
                        elif (no_whitespace.startswith("}") or no_whitespace.startswith("]")) and len(no_whitespace) == 1:
                            mapping = False
                            extras = False
                            defaults = False
                            continue
                        
                        if no_whitespace == "" or no_whitespace.startswith("#"):
                            continue
                        
                        if mapping:
                            if not line in relevant_configs["mapping"]:
                                relevant_configs["mapping"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        elif extras:
                            if not line in relevant_configs["extras"] or no_whitespace == "}),":
                                relevant_configs["extras"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        elif defaults:
                            if not line in relevant_configs["defaults"]:
                                relevant_configs["defaults"].append(line)
                            elif not line == "\n":
                                reset_settings()
                                return (False, line)
                        else:
                            if not line in relevant_configs["non_cmd"]:
                                relevant_configs["non_cmd"].append(line)
                    
        # At this point, either we have all the lines or the function is returned False
        with open(paths.get_generic_config_path() + "\\combined\\config.txt", "w+") as fw:
            for lnc in relevant_configs["non_cmd"]:
                fw.write(lnc)
            fw.write("cmd.mapping= {\n")
            for lm in relevant_configs["mapping"]:
                fw.write(lm)
            fw.write("}\n")
            fw.write("cmd.extras= [\n")
            for le in relevant_configs["extras"]:
                fw.write(le)
            fw.write("]\n")
            fw.write("cmd.defaults= {\n")
            for ld in relevant_configs["defaults"]:
                fw.write(ld)
            fw.write("}\n")
        
        return True
    except Exception:
        utilities.report(utilities.list_to_string(sys.exc_info()))
    
    
    
    
def camel_case(text):
    t = str(text)
    words = t.split(" ")
    Text(words[0] + "".join(w.capitalize() for w in words[1:]))._execute()
    
def score(text):
    """ score <dictation> """  # Docstring defining spoken-form.
    t = str(text)  # Get written-form of dictated text.
    Text("_".join(t.split(" ")))._execute()
