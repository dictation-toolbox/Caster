# Contributing

*How can I help?*

1. **Write code.** There is [a lot which needs to be done](https://github.com/dictation-toolbox/caster/issues). If you can program in Python, please write some code. There are also a lot of [open pull requests](https://github.com/dictation-toolbox/Caster/pulls) that need changes, testing, or a close review.
2. **Write documentation.** The [ReadTheDocs page](http://caster.readthedocs.org/en/latest/) is pretty sparse. ReadTheDocs uses [markdown](https://markdown-guide.readthedocs.io/en/latest/) so create new docs as .md files.
3. **Speak.** Tell others who might be interested in Caster. Join our discussions on the issues page and [Gitter](https://gitter.im/dictation-toolbox/caster). The more the merrier, and your thoughts are welcome and encouraged.

## Only start major contributions if you will commit to them
Many newcomers to the voice coding community are expert developers who arrive very excited to make a fundamental contribution to this project or create something that will supersede Caster. If this is you, great! However, the vast majority of these contributions have gone nowhere, because the developer loses interest and the project is not in a place to be picked up by someone else; we do not want _this_ to be you. We encourage you to address one of the existing issues or review/finish a pull request. If you really do want to make a major contribution, please first [raise an issue](https://github.com/dictation-toolbox/Caster/issues/new/choose) with your idea.

## Adding New Rules for the Caster repository
If you'd like to add rules for new languages or popular libraries for languages for the Caster repository, you should create them in the `castervoice/rules` folder in the appropriate directory category.

## BountySource Guidelines
- In order for bounties to be posted they must have very clear guidelines and resources for those that wish to collect.

- While you can post bounties as an individual, it's best to work with community to develop them. Therefore we request that each bounty candidate be discussed with the community in a GitHub issue.

## Caster GitHub Workflow

It is recommended that you review one of the many online tutorials (for example, [this one](http://yangsu.github.io/pull-request-tutorial/)) to familiarize yourself with the standard GitHub workflow.

This guide assumes that you would [make your own fork](https://help.github.com/articles/fork-a-repo/) of the Caster repository. You can clone your copy locally and setup a remote pointing to the upstream (dictation-toolbox) repository. Once your fork is created, these are some basic commands to get you started: 

    cd C:\MyProjects
    git clone https://github.com/{YOUR-USER-NAME}/caster/
    cd caster
    git remote add upstream https://github.com/dictation-toolbox/caster/


### Prepare a feature branch for your pull request

Fetch the latest from the upstream (dictation-toolbox) repo:

    git fetch upstream

Create a new branch for your PR:

    git checkout --no-track -b <pr-feature-name> upstream/master

Where **`<pr-feature-name>`** is the name you want to give to your new feature branch.


### Make your changes and commit them to your PR branch:

    edit somefile.txt
    edit anotherfile.cpp
    git commit -a -m "Made some changes..."


### Push your PR branch up to your GitHub fork:

    git push origin pr-feature-name


### Open a pull request

When you navigate to your fork on GitHub, you will be asked if you want to open a pull request for the branch you just pushed. Click the button to open a new pull request and make sure you select the `master` branch on the base (dictation-toolbox) fork. Then fill out the PR template that will appear. 
