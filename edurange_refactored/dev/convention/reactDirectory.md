

The convention for directories involving react is:

- lowercase_snake always with directories 
this is to avoid pointless annoyances and cross-language formatting problems

edurange_refactored
    /react
        /pages
            /home
                README.md
                home.index.js
                /src
                    HomeRouter.js
                    Home.js
                    Home.css

                    /components
                        /login
                            Login.js
                            Login.css
                        /logout
                            Logout.js
                            Logout.css
                        
                /dashboard (shallower)
                    /src
                        Dashboard.js
                        Dashboard.css
                        /components
                            DashboardChild.js
                            DashboardChild.css
                    /scenarios 
                        etc.....

...the important point here is that there are NO files in the 'top-level' directory of any "page"...
...apart from an optional README.md and possibly a <pageName>.index.js file...
...everything else will either be behind /src or one of the traversal subdirectories like /dashboard...
...and the 'components' directory is always inside '/src' if it even exists (not all pages need it)...
...you should think of 'components' more in the common language sense here, as in a piece of a whole...

there is a method to the madness

first of all, there is a 1:1 relationship between directory traversal here and 
URL traversal in the webapp beyond the /pages directory (at least for major directory tiers)
    (...for deeper nested, or dead-end child "components", URL may still be on parent.)
    
    for example:  /home  will be either `edurange.org:5000/` or, in development, `edurange.org:5000/edurange3/`
            
            beyond that, /pages/home/examplePage  would be 
                `edurange.org:5000/examplePage` 
                or 
                `edurange.org:5000/edurange3/examplePage`

(note: again, 'component' refers to small parts of a 'page' which don't comprise their own page.
for example, a login box within the Login.js screen is a component of the Login page, but isn't a page itself, 
so doesn't get a directory. Or a 'card' within a 'card list' would be a 'component' where the 'card list' is a 'page'.)  it is a loose definition.

Or in the case of components that do make their own page, or have too many associated files,
but are total dead-ends and 'feel like' they belong to the parent, those can go inside a 
separate directory in 'components'. e.g. Login and Logout could go in Home.js as 'components', 
even if they are technically their own 'page'.

yes, there is some subjectivity when you get down to that level, but the important part is that
everything that is part of loading a page, or nearby page children go in /src, and any 'parts of'
the page go in /src/components

IMPORTANT: there never should be more than 1 `src` or 1 `components` in any directory path, but ALL
           actual React "Component.js" type files must be in a /src directory somewhere.
           the point is to help people tell what is a continuation of the directory path and what is
           the actual local 'page' source files. if your local component files are always in /src, 
           there will never be any confusion.

that can be done by using this logic:

    - the directory/URL itself is for traversal
    
    - when the directory/URL matches the place where the component should be, 
        the next path is /src/ and that's where the files that are specific to that actual
        component will go.
          - so for example, in /home, everything that is in the /home/src directory are things
            that belong only to that component (including any children that it is rendering)

            e.g. pages/
                        home/
                            src/
                                Home.js
                                Home.css
                        info/
                            src/
                                Info.js
                                Info.css
    
    - in the /src directory, the primay React .js Component file will reside alongside 
        its .css pairing.  
    
    - if there are more pieces that need to be rendered, then you create an extension of /components
        (in this context, the word "components" should be thought of in the common usage sense, as in a part of a whole)

            e.g. pages/
                        home/
                            src/
                                Home.js
                                Home.css

                                components/
                                    Login.js
                                    Login.css

                        info/
                            src/
                                Info.js
                                Info.css
    
    - if you decide that the Login.js component (or concept) is too big, then you can make a
        directory under `components` to match the name of the child component

            e.g. pages/
                        home/
                            src/
                                Home.js
                                Home.css

                                components/
                                    login/
                                        Login.js
                                        Login.css

                        info/
                            src/
                                Info.js
                                Info.css
    
These rules are a bit complex but thought was put in and they will help keep things cleaner and saner.
            