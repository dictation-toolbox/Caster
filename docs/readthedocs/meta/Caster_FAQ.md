## **Caster Frequently Asked Questions - FAQ**

Welcome to the Caster project! This FAQ guide this to help introduce the Caster project and the community. 

1. **What type of individuals are in the Caster community?**  

      Individuals involved in the Caster project are incredibly diverse. In the community people are from all over the world. We are representative of the UK, US, Australia, Canada, Germany, and other countries.

      What we all have in common is we want to leverage our voice to enhance our computing experience. People come to the project for different reasons. There are medical reasons that may limit people's ability to interact with the keyboard and mouse. On the other side of the spectrum, there are those that augment their workflow with voice controlling applications in combination with traditional computer inputs. 
      
      

2. **Is Caster only meant to be used by developers who code only by voice?**

      Both developers and everyday users can benefit from a simple experience to control their computer. Caster was designed for voice programmers who develop software. However programming is a barrier for most people. We want to simplify experience for the everyday users, yet maintain the power and flexibility necessary for developers underneath the hood. 

      Caster can be used without programming experience and customized on a basic level through simplified transformers. Which allow you to redefine command names without programming experience. We acknowledge there is a lot of work to be done to make Caster truly accessible for those without a technical background, but that vision is a work in progress.
      
      

3. **Maybe I do not need certain features. How flexible is Caster?** 

      The voice commands are purposely structured to allow you to pick and choose how you want to use the project. This allows for a broad userbase with diverse interests and abelites.  A configuration file allows you to block categories of commands called `rules`  giving you control over your experience. The sky is the limit. Consider the following use cases:

      - I am developer or person who does not have barriers using computer inputs like keyboard and mouse. I only want to control applications by voice to augment their workflow.

        You can disable all the rules that are related to voice programming, advanced mouse and keyboard control.

      - I need a highly customized environment to build own custom rules that suits my needs.

        You could disable all the starter rules and create your own with Caster as a framework.
        
        

4. **Why does the Caster use obscure or strange words for command names?**

      Typically speech recognition engines are great with sentences not short commands. Basically the general vocabulary is too ambiguous for speech recognition engines to discern between words that are phonetically close and how they are pronounced. Think of how similar "end", "and", "n" and "m" sound, and if that's all you heard and did not know the context of it being in a sentence. Words that are phonetically distinct from each other increase speech recognition accuracy.  

      

5. **Can I customize the rules that contain voice commands in Caster?**

      Customization of command phrases is expected. Many people customize commands due to preference or if commands are not pronounceable in their dialect. Everyone's voice, microphone, soundcard, speech engine backend and dictation environment is different. There are distinct advantages for creating your own commands.

      - Customizing commands will lead to higher accuracy 
      - Commands that are created by the end-user are more likely to be remembered

      You can customize commands by copying starter rules, utilizing simplified transformers, or creating your own from scratch. See the read the `Caster Rules` in the documentation.
      
      

6. **Does Caster support multiple languages?**

      Currently the starter rules are structured on the English language. If your speech recognition supports your language, you can customize them to your preference. In order to make Caster starter rules Multilingual, the project needs a proper [grammar API](https://github.com/dictation-toolbox/Caster/issues/533#issuecomment-589829408).
      
      
      
7. **Does Dragonfly come with its own commands?**

      Dragonfly does not come with built-in commands, and you would have to to create their own commands.

      

8. **What's the difference between Caster and Dragonfly?**

      Caster is built on top of Dragonfly. Caster adds some significant features that Dragonfly does not have.

      - Caster reloads rules on save automatically

      - Caster has continuous command recognition (CCR) MergeRules

      - NodeRule allows packing specs into nodes in a tree and only activating part of the tree at a given time without overwhelming the speech recognition engine. It's possible to include thousands of specs in a single grammar.

      - RegisteredAction and ContextSeeker allow you to change command behavior based on previous recognized commands or future commands that are available.

        

      Outside of those features, Caster really only differs from the Dragonfly framework on how grammars are loaded and their context created. Otherwise it simply adds functionality. 99% of what you can do in Dragonfly can be done in Caster as well.

