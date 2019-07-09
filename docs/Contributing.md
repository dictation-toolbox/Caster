# Contributing

*How can I help?*

1. **Write code.** There is [a lot which needs to be done](https://github.com/dictation-toolbox/caster/issues). If you can program in Python, please write some code. There are also a lot of [open pull requests](https://github.com/dictation-toolbox/Caster/pulls) that need changes, testing, or a close review.
2. **Write documentation.** The [ReadTheDocs page](http://caster.readthedocs.org/en/latest/) is pretty sparse. ReadTheDocs uses [markdown](https://markdown-guide.readthedocs.io/en/latest/) so create new docs as .md files.
3. **Speak.** Tell others who might be interested in Caster. Join our discussions on the issues page and [Gitter](https://gitter.im/dictation-toolbox/caster). The more the merrier, and your thoughts are welcome and encouraged.

### BountySource Guidelines
- In order for bounties to be posted they must have very clear guidelines and resources for those that wish to collect.

- While you can post bounties as an individual it's best to work with community to develop them. Therefore we request that each bounty candidate be discussed with the community in an issue with a minimum of seven days for feedback before the it gets posted.

## Caster GitHub Workflow

It is recommended that you review one of the many online tutorials (for example, [this one](http://yangsu.github.io/pull-request-tutorial/)) to familiarize yourself with the standard GitHub workflow.

This guide assumes that you have already forked the Caster repository, cloned your copy locally, and setup a remote pointing to the upstream (dictation-toolbox) repository. This setup process is covered [here](https://help.github.com/articles/fork-a-repo/), but essentially consists of creating a fork on GitHub, followed by something like the following sequence of commands to make a local copy of the repository and link it back to the upstream (dictation-toolbox) fork:

    cd C:\MyProjects
    git clone https://github.com/{YOUR-USER-NAME}/caster/
    cd caster
    git remote add upstream https://github.com/dictation-toolbox/caster/


### Prepare a feature branch for your pull request

Fetch the latest from the upstream (dictation-toolbox) repo:

    git fetch upstream

Create a new branch for your PR:

    git checkout --no-track -b pr-feature-name upstream/master

Where **`pr-feature-name`** is the name you want to give to your new feature branch.


### Make your changes and commit them to your PR branch:

    edit somefile.txt
    edit anotherfile.cpp
    git commit -a -m "Made some changes..."


### Push your PR branch up to your GitHub fork:

    git push origin pr-feature-name


### Open a pull request

When you navigate to your fork on GitHub, you will be asked if you want to open a pull request for the branch you just pushed. Click the button to open a new pull request, enter a title and description for the PR, and make sure you select the `master` branch on the base (dictation-toolbox) fork.


