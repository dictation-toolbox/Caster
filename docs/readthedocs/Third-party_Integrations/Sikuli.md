# Sikulix Integration

[This is Sikulix](http://sikulix.com/). Caster can launch Sikulix actions by voice.

## Versions

At time of writing, Caster supports Sikulix v2.0.1 and up. 

## Setup

### Sikulix v2.x.x

- Requires on Python 2 to be installed when using `jython-standalone-2.7.x`
- Install 64-Bit Java 8+ and check the Java path with the following command:

```text
    java -version
```

- Download sikulix.jar: `jython-standalone-2.7.x.jar`
- Place the two jars next to each other in a folder. The folder location location does not matter.
- Edit settings.toml `C:\Users\%USERNAME%\AppData\Local\caster\settings\settings.toml`:

```toml
    [paths]
    SIKULI_IDE = "full/path/to/sikulix.jar"
    SIKULI_RUNNER = "full/path/to/sikulix.jar"

    [sikuli]
    version = "2.0.1"
    enabled = true
```

- Sikulix will start next time Dragon Restarts.
- Make commands with filename/"exports" convention as per the video. 

## Script Creation Conventions

This video is out of date in terms of the Sikuli setup and config options. It is still up to date for the filename/exports convention described toward the end of the video though.

[![](http://img.youtube.com/vi/RFdsD2OgDzk/0.jpg)](http://www.youtube.com/watch?v=RFdsD2OgDzk "Sikuli Commands by Voice: Script Creation Conventions")

## Control Sikulix

- Say `enable sikuli control` to make the following commands available.
  - "launch sick IDE" - Launches Sikulix's integrated IDE for Sikulix Scripts
  - "launch sick server": Launches `Caster Sikuli Bridge` for controlling your custom scripts scripts by voice
  - "terminate sick server": Closes the `Caster Sikuli Bridge`
  - "refresh sick server" Restarts the `Caster Sikuli Bridge`