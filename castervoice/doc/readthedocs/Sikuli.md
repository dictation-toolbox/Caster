# Sikuli Integration

[This is Sikuli](http://sikulix.com/). It's awesome, and you can use Caster to launch Sikuli actions by voice.

## Versions

At time of writing, Sikuli [1.1.3 is no longer supported](https://raiman.github.io/SikuliX1/downloads.html), but [1.1.4 is not yet released](https://launchpad.net/sikuli/sikulix). So pick your version. Caster currently supports both.

## Setup

### Sikuli v1.1.3

- install Java 8+, make sure it's on your path with:

```
    java -version
```

- download sikulixsetup-1.1.3.jar
- run it, choose option 1
- Edit settings.toml `C:\Users\%USERNAME%\.caster\data\settings.toml`:

```toml
    [paths]
    SIKULI_IDE = "full/path/to/sikulix.jar"
    SIKULI_RUNNER = "full/path/to/runsikulix.cmd"
    [sikuli]
    version = "1.1.3"
    enabled = true
```

- make commands with filename/"exports" convention as per the video

### Sikuli v1.1.4:

- install Java 8+, make sure it's on your path with:

```
    java -version
```

- download sikulix.jar, jython-standalone-2.7.1.jar
- place the two jars next to each other
- Edit settings.toml `C:\Users\%USERNAME%\.caster\data\settings.toml`:

```toml
    [paths]
    SIKULI_IDE = "full/path/to/sikulix.jar"
    SIKULI_RUNNER = "full/path/to/sikulix.jar"
    [sikuli]
    version = "1.1.4"
    enabled = true
```

- make commands with filename/"exports" convention as per the video

## Script Creation Conventions

This video is out of date in terms of the Sikuli setup and config options. It is still up to date for the filename/exports convention described toward the end of the video though.

[YouTube](https://youtu.be/RFdsD2OgDzk?list=PLV6JPhkq1x8LHu02YefhUU9rXiB2PK8tc)
