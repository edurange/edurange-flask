
This 'templates' directory represents the root directory of the website, and 'pages' that are available from the 
root url (eg 'edurange.org/info') should be children of this directory (it is not entirely the case at this point)

practically, the better name for the directory would be in fact 'pages', and I would just think of the 'templates'
directory that way. 

the main exception to this is the 'main_frame' directory, which is essentially the component which acts as the 
frame around the home component. MainFrame.js acts as the main router for the app, but isn't the actual 'route' that 
people will try to visit when they either go to the home page or when they click a link, so it's an exception.

In other words, when people visit edurange.org/ , it will be MainFrame.js doing the routing.

'public' is another exception, and it's just a normal resources directory.

another exception is 'utils' and it seems to mostly be related to legacy stuff, so i'm not touching that :)

the last very important exceptions is the 'entry' directory and its associated EduRangeEntry.js script, 
which together are the primary entry point for the entire EduRange-React app.

from there, they serve up the MainFrame.js router, which takes control of the edurange.org base '/' path. 

e.g. MainFrame.js serves up edurange.org/info by way of react-router.

the edurange.org/dashboard/ extension root is served up by DashRouter.js, and similar schemata will apply 
for edurange.org/info and certain other routes like that