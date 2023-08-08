
///////////////////////
////// EduRangeEntry.js is the primary Main Entry script for EduRange-React
////// Acts more or less as an App.js would in normal React contexts
////// Should be kept as clean as possible
///////////////////////

// MainFrame.js is the secondary main entry point Component.

MainFrame does most of the routing and framing of the nav components and things of that nature upon initial visit.
MainFrame also serves up LOGGED OUT data and the login page with and redirection to the tertiary entry point, 
which serves up LOGGED IN functionality, which is the /dashboard/ route URL

At this time, the dashboard is DashRouter.js