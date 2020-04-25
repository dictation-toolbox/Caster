import dragonfly
import sys


class CCRType(object):
    GLOBAL = "global"
    APP = "app"
    SELFMOD = "selfmod"


# default-on modules
CORE = [
    # Original Caster CCR "core" set:
    "Alphabet", "Navigation", "NavigationNon", "Numbers", "Punctuation",
    # Rules which were split out of _caster.py:
    "CasterRule", "HardwareRule", "MouseAlternativesRule", "WindowManagementRule",
    # Alternate mouse grid controls:
    "DouglasGridRule", "RainbowGridRule", "SudokuGridRule",
    # HMC GUI control rules:
    "HMCRule", "HMCConfirmRule", "HMCDirectoryRule",
    "HMCHistoryRule", "HMCLaunchRule", "HMCSettingsRule",
    # GUI Rules
    "HistoryRule", "ChainAlias", "Alias",
    # other common rules
    "BringRule", "Again"
    ]

# default-on modules that are platform or engine specific
if sys.platform == "win32":
    CORE.extend([
         "LegionGridRule",
         "IERule"
    ])
    # get_engine() is used here as a workaround for running Natlink inprocess
    if dragonfly.get_engine().name == 'natlink':
        CORE.append("DragonRule")

# internal rules
INTERNAL = [
    "GrammarActivatorRule", "HooksActivationRule", "TransformersActivationRule",
    "ManualGrammarReloadRule"
]

# default companion rules
COMPANION_STARTER = {
    "Navigation": ["NavigationNon"],
    "Java": ["JavaNon"],
    "Matlab": ["MatlabNon"],
    "Prolog": ["PrologNon"],
    "Python": ["PythonNon"],
    "Rust": ["RustNon"],
    "VHDL": ["VHDLnon"],
    "EclipseCCR": ["EclipseRule"],
    "VSCodeCcrRule": ["VSCodeNonCcrRule"]
}
