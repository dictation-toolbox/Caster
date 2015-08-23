## About Dragonfly and 64-bit Executables

### Problem, Solution

Presently, the [version of Dragonfly from the main repo](https://github.com/t4ngo/dragonfly) has trouble reading 64-bit executable names. Daanzu's patch fixes this problem, but the [pull request](https://github.com/t4ngo/dragonfly/pull/41) has been inactive for 4 months at time of writing. **[This fork of dragonfly](https://github.com/synkarius/dragonfly) includes the patch**, and should be used in place of the main repo version until the patch is either accepted or rejected.

### Why Does It Matter?

Things like focusing windows, or commands which use process names won't work without the patch.

### What's the Difference?

[Have a look for yourself.](https://github.com/t4ngo/dragonfly/pull/41/files)