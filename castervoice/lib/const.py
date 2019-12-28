class CCRType(object):
    GLOBAL = "global"
    APP = "app"
    SELFMOD = "selfmod"


# default-on modules
CORE = [
    # original Caster CCR "core" set:
    "Alphabet", "Navigation", "Numbers", "Punctuation",
    # rules which were split out of _caster.py:
    "CasterRule", "HardwareRule", "MouseAlternativesRule", "WindowManagementRule",
    # alternate mouse grid controls:
    "LegionGridRule", "DouglasGridRule", "RainbowGridRule", "SudokuGridRule",
    # gui control rules:
    "HMCRule", "HMCConfirmRule", "HMCDirectoryRule",
    "HMCHistoryRule", "HMCLaunchRule", "HMCSettingsRule",
    # other common rules
    "DragonRule", "BringRule"
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
