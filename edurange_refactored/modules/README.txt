

this new 'edurange_refactored/modules' directory is for FRONT-END-ONLY related higher order scripts, 
object indexes, react-routing and other universal (front-end-restricted) things of that nature. 
they should be further categorized into child directories.

all higher order things in any way backend related, including backend routes and auth schemas, 
which are used by the front-end, should be in '/edurange_refactored/api/example', not here.

note: at this time, the exact structure of this directory is still a WIP

/instructor : scripts and data relating to instructor specific functionality 
/scenarios  : scripts and data relating to user-scenario interaction, mostly about the 'guide' page (questions/answers) 
/shells     : class constructor shells of all kinds, populated with some autoinitializing values and some default. takes input object to apply input to properties 
/ui         : for UI related functionality, such as icon definitions and imports, link sets, etc. 
/routing    : (will be changes to '/routes') everything related API calls to the flask backend that doesn't for a good reason belong in the individual components should go here 
