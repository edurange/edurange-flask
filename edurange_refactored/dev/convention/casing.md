

camelCase
- `camelCase` always with conjoined words in JS that are *not* React Components. especially variables.
- in general, if you are making a file that is mostly associated with the .js ecosystem, and there's no specific reason otherwise, use `camelCase`.  ifItGetsTooLong_youCanBreakItUp_withSnakeBreaks

kebab-case
- `lower-kebab-case-always` with css and html, unless there's a good reason otherwise
- avoid `kebab-casing` (upper and lower) altogether in both React and Flask. it gets interpreted as subtraction sometimes. 

PascalCase
- `PascalCase` always with ReactComponents.

lower_snake_case
- `lowercase_snake` always with directories.  
- use `_snake` prefices / suffices for "flags" in React, such as `_isActive` or `set_` 
- however, when using `_snake` flags, conjoined phrases like loggedIn remain `camelCase`
  e.g. `set_isActive_state`. Here `isActive` is the "real" variable, and `set_` and `_state` are flags.
- there is no single way to do this, but `set_isActive` is more clear than `set_is_active`, by a lot
- in other words, `_snake casing` in React is only for flags_ 
- the exception for that is `veryLongVariables_youNeedToBreakUp`, which again use a combination of camel and snake

- in flask, `lower_snake_case_is_safest`
- whenever making queries between React and Flask, `lower_snake_case_is_safest`
- when making urls (and therefore routes), `lower_snake_case_is_practically_required`

SCREAMING_SNAKE_CASE
- only for certain configuration file variables and sometimes enums. you'll know.
