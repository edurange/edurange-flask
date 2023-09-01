

"Entry" means the place where an app (in this case React) initially inserts itself into
the broader program (here, it's Flask).  In this case, EduRangeEntry.js, the React component, is doing so
by way of a queryselectory and root.render method, 
attaching itself to `edurange_refactored/templates/public/edurange3_entry.html` 
in the <div id="edurange3_entry_id"> element

From there, EduRangeEntry passes control of the whole frontend to HomeRouter.js,
which should be considered the primary facilitator for the edurange3-react webapp.

In other words, there is only 1 point where .html is transfered from the backend, and it is
to serve `edurange_refactored/templates/public/edurange3_entry.html` to the browser on initial visit (or refresh).

the EduRangeEntry.js file acts more or less as an App.js would in normal React contexts,
except that we do not need to initialize any additional library instances other than react-router.
In general, it should be kept as clean as possible
