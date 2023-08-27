

camelCase

  - `camelCase` with conjoined words in JS/React that are *not* 
  React Components. especially variables.

  - in general, if you are naming something that is mostly associated with 
  the .js/React ecosystem, and there's no specific reason otherwise, 
  use `camelCase`.  ifItGetsTooLong_youCanBreakItUp_withSnakeBreaks


kebab-case

  - `lower-kebab-case-always` with css and html, unless there's a good 
  reason otherwise

  - avoid `kebab-casing` (upper and lower) altogether in both React 
  and Flask. it gets interpreted as subtraction sometimes. 


PascalCase

  - `PascalCase` with ReactComponents - both the .js file and the Function().


lower_snake_case

  - `lowercase_snake` always with directories.  

  - use `_snake` prefices / suffices for "flags" in React, 
  such as `_state` or `set_` 

  - however, when using `_snake` flags, conjoined phrases like 
  isActive remain `camelCase`

    e.g. `set_isActive_state`. Here `isActive` is the "real" variable, 
    and `set_` and `_state` are flags.

  - There is ofc no single way to do this, but I think you'll agree
   `set_isActive` is more clear than `set_is_active`, by a lot...

  - in other words, `_snake casing` in React is mostly for flags_ 

  - the main exception for that is `veryLongVariables_youNeedToBreakUp`, which 
  again use a combination of camel and snake

  - in flask, `lower_snake_case_is_safest`

  - whenever making queries between React and Flask, `lower_snake_case_is_safest`

  - when making urls (and therefore routes), `lower_snake_case_is_practically_required`



SCREAMING_SNAKE_CASE
  - Only for certain configuration file variables and sometimes enums. 
  Don't worry, you'll know.
