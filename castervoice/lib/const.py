class CCRType(object):
    GLOBAL = "global"
    APP = "app"
    SELFMOD = "selfmod"


# default-on ccr modules
CORE = ["Alphabet", "Navigation", "Numbers", "Punctuation"]

# default companion rules
COMPANION_STARTER = {
    "Navigation": "NavigationNon",
    "Java": "JavaNon",
    "Matlab": "MatlabNon",
    "Prolog": "PrologNon",
    "Python": "PythonNon",
    "Rust": "RustNon",
    "VHDL": "VHDLnon",
    "EclipseCCR": "EclipseRule",
    "FlashDevelopCCR": "FlashDevelopRule",
    "VSCodeCcrRule": "VSCodeNonCcrRule"
}
