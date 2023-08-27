

Backend logic ideally should be kept relatively piecemeal so 
that the scripts can be re-used in different React components, 
and even different UIs entirely at some point.

So in other words, instead of creating a big (Flask)
helper function which grabs a bunch of things, does a bunch 
of processing, and returns a prepared return, it is usually 
better to compartmentalize each of the steps as much as 
reasonably possible in flask, and then create 'business logic' 
helper functions and scripts in JS to call upon those pieces 
as they're needed.

In addition, when making the helper modules/scripts in JS, you 
should once again try to decouple the business logic functions 
as much as reasonably possible from the actual presentation 
logic, so that the scripts can be re-used.

For example, if you are building a table of scenarios, or 
building a complete object that represents a single scenario, 
it is often best to create a separate JS module that will call 
the neccessary routes one at a time, arrange the data it receives 
as necessary, then return it your component.

When you return the data to your component, try to do it in a 
format that you think can be most easily reused by other devs 
and components project-wide, rather than tailoring it so specifically 
to your component that no other components can benefit from your hard 
work.  Obviously, this won't always be feasible.

Inside your component, once you receive your data, then that is 
where you would further tailor it, and assign it to your specific 
UI presentation.