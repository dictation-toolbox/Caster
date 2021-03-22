# Choose a Speech Recognition Engine

Caster currently supports the following speech recognition engines on Microsoft Windows Vista through Windows 10. This is a brief overview of the supported speech recognition engines.

## Dragon NaturallySpeaking

**Dragon [NaturallySpeaking (DPI)](https://www.nuance.com/dragon.html)** - Caster supports Dragon NaturallySpeaking 13 (DNS) or higher. For best results, Dragon Professional Individual (DPI) is recommended.

- Known for its high accuracy in speech recognition especially with free dictation.

- Has support from multiple accents and dialects

- User Profile management and local vocabulary training

- Polished GUI

- Superior Background noise rejection. Distinguishes speech from background noise.

Disadvantages

- Closed source speech recognition engine
- Expensive $300 DPI and Dragon NaturallySpeaking Home (DNS) $150 (Note DNS limitations below)
- Will never have native cross-platform support by Nuance.
- Cannot use custom speech recognition models
- Zero low level access to the engine implementation

**Dragon NaturallySpeaking Home** **(DNS)** can be used by Caster however comes with significant limitations besides what's mentioned in their [matrix comparison](https://www.dragonsupportservice.us/dragon-15-home-vs-professional-specifications/) and therefore not recommended. The retail upgrade cost DPI is about the same as the Dragon NaturallySpeaking Home. 

Limitations of the Home Edition include but not limited to:

- Does not include vocabulary editor to edit/add/delete words for recognition.

- Cannot add new DNS commands (You can add new commands created with Dragonfly)

- Lacks built-in command/dictation/spell/number modes. Using `command mode` is recommended when programming by voice.

- Lacks many other settings to customize DNS for productivity.

## Kaldi

Daanzu's [Kaldi](https://dragonfly2.readthedocs.io/en/latest/kaldi_engine.html) open source engine cross-platform speech recognition based on [Kaldi Project](https://kaldi-asr.org/).  

- Free and open source engine that respects user privacy.

- Typically lower recognition latency than DNS

- A selection of pre-trained speech recognition models to choose from that are continually developed.

- It's possible to use a data set with your own voice to train your own model if you have the necessarily technical skills and equipment.

- Custom recognition weights for Grammar/Rule/Element

- Low level access to speech engine and parameters that are customizable unlike DPI or WSR.

- Optionally uses cloud-based machine learning to produce pronunciation's for unknown words

- Alternative Dictation sources such as a cloud based or local speech recognition backend

- Many other highlights can be found in Daanzu's [Kaldi Documentation](https://dragonfly2.readthedocs.io/en/latest/kaldi_engine.html)

Disadvantages

- Does not have a GUI for editing vocabulary (User Lexicon) but can be easily edited through txt file.
- Currently does not support training the user lexicon speech recognition model locally.
- Mileage may vary but typically free dictation accuracy is lower than DNS/DPI.

## Windows Speech Recognition

[Windows Speech Recognition](https://support.microsoft.com/en-us/help/4027176/windows-10-use-voice-recognition) (WSR) - Not Microsoft Cortana

- Free

- Simple to set up with the least dependencies

- Preinstalled on all supported Windows OS

  Disadvantages

- With Caster WSR built-in commands are not available and does not utilize WSR's GUI.

- Least accurate with free dictation and commands
- Not actively developed by Microsoft
- Will never have native cross-platform support by Microsoft.
  - Cannot use custom speech recognition models
- Zero low level access to the engine implementation
