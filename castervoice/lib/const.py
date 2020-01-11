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
    "LegionGridRule", "DouglasGridRule", "RainbowGridRule", "SudokuGridRule",
    # HMC GUI control rules:
    "HMCRule", "HMCConfirmRule", "HMCDirectoryRule",
    "HMCHistoryRule", "HMCLaunchRule", "HMCSettingsRule",
    # GUI Rules
    "HistoryRule", "ChainAlias", "Alias",
    # other common rules
    "DragonRule", "BringRule", "Again",
    ]

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
