
// these are used by some menus to define what their label, icon, and link path should be
// at the bottom, arrays define which items should be displayed in which contexts
// you can simply add some more and use them as you wish

// the navStub is used by Home_router.js and Dashboard_router.js (among others)
// to determine which set of navigation items to show upon navigation
// by inserting the stub into a dict reference in order to point to a given navArray (at bottom)

// the array of nav objects is then passed to HomeHead.js or DashSideNav.js as a prop.

import edurange_icons from "../ui/edurangeIcons";

const home = {
    title: "Home",
    icon: edurange_icons.home,
    path: `/edurange3`,
    navStub: 'home'
};
const login = {
    title: "Login",
    icon: edurange_icons.user_check,
    path: `/edurange3/login`,
    navStub: 'home'
};
const logout = {
    title: "Logout",
    icon: edurange_icons.user_x,
    path: `/edurange3/dashboard/logout`,
    navStub: 'home'
};
const info_home = {
    title: "Info",
    icon: edurange_icons.book,
    path: `/edurange3/info`,
    navStub: 'home'
};
const docs = {
    title: "Docs",
    icon: edurange_icons.book,
    path: `/edurange3/info/docs`,
    navStub: 'home'
};
const about = {
    title: "About",
    icon: edurange_icons.book,
    path: `/edurange3/info/about`,
    navStub: 'home'
};
const contact = {
    title: "Contact",
    icon: edurange_icons.book,
    path: `/edurange3/info/contact`,
    navStub: 'home'
};
const help = {
    title: "Help",
    icon: edurange_icons.questionmark,
    path: `/edurange3/info/help`,
    navStub: 'home'
};
const options = {
    title: "Options",
    icon: edurange_icons.gear,
    path: `/edurange3/options`,
    navStub: 'options'
};
const themes = {
    title: "Themes",
    icon: edurange_icons.palette,
    path: `/edurange3/options/themes`,
    navStub: 'options'
};
const accessibility = {
    title: "Accessibility",
    icon: edurange_icons.accessibility,
    path: `/edurange3/options/accessibility`,
    navStub: 'options'
};
const dashboard = {
    title: "Dashboard",
    icon: edurange_icons.computer_monitor,
    path: `/edurange3/dashboard`,
    navStub: 'dash'
};
const admin = {
    title: "Admin",
    icon: edurange_icons.admin,
    path: `/edurange3/dashboard/admin`,
    navStub: 'dash_admin'
};
const instructor = {
    title: "Instructor",
    icon: edurange_icons.instructor,
    path: `/edurange3/dashboard/instructor`,
    navStub: 'dash_instructor'
};
const account = {
    title: "Account",
    icon: edurange_icons.account,
    path: `/edurange3/dashboard/account`,
    navStub: 'dash'
};
const scenarios = {
    title: "Scenarios",
    icon: edurange_icons.chess_knight,
    path: `/edurange3/dashboard/scenarios`,
    navStub: 'dash'
};
const notifications = {
    title: "Notifications",
    icon: edurange_icons.bell,
    path: `/edurange3/dashboard/notifications`,
    navStub: 'dash'
};
const ssh = {
    title: "Connect via SSH",
    icon: edurange_icons.terminal_prompt,
    path: `/edurange3/dashboard/ssh`,
    navStub: 'dash'
};
const sshweb = {
    title: "webSSH",
    icon: edurange_icons.terminal_prompt,
    path: `/edurange3/dashboard/sshweb`,
    navStub: 'dash'
};
const instructor_userGroups = {
    title: "Student Groups",
    icon: edurange_icons.userGroup,
    path: `/edurange3/dashboard/userGroups`,
    navStub: 'dash_instructor'
};
const instructor_scenarioGroups = {
    title: "Scenario Groups",
    icon: edurange_icons.scenarioGroup,
    path: `/edurange3/dashboard/scenarioGroups`,
    navStub: 'dash_instructor'
};
const instructor_users = {
    title: "Students",
    icon: edurange_icons.user,
    path: `/edurange3/dashboard/users`,
    navStub: 'dash_instructor'
};
const jwt_test = {
    title: "jwt_test",
    icon: edurange_icons.key,
    path: `/edurange3/dashboard/jwt_test`,
    navStub: 'dash'
};

export const navArrays = {

//logged_out
    side_logout:            [ jwt_test, home, docs, options, login, logout ],
    top_logout:             [ jwt_test, home, docs, options, login, logout ],

//home  
    side_home:              [ home, dashboard, scenarios, notifications, docs, options, account, logout , help, login ],
    top_home:               [ jwt_test, home, dashboard, options, account, logout, login ],

//options
    side_options:           [ accessibility, themes, home ],
    top_options:            [ jwt_test, home, dashboard, options, account, logout, login ],

//dashboard
    side_dash:              [ home, dashboard, scenarios, instructor, admin, notifications,  options, account, logout ],
    top_dash:               [ jwt_test, home, dashboard, notifications,   options, account, logout, login ],

//guide
    side_guide:              [ home, dashboard, scenarios, ssh, instructor, admin, notifications,  options, account, logout ],
    top_guide:               [ jwt_test, home, dashboard, scenarios, ssh, notifications,   options, account, logout, login ],

//admin-dashboard
    side_dash_admin:        [ home, dashboard, scenarios, instructor, admin, notifications,  options, account, logout ],
    top_dash_admin:         [ jwt_test, home, dashboard, notifications,   options, account, logout, login ],

//instructor-dashboard
    side_dash_instructor:   [ home, dashboard, scenarios, instructor, admin, notifications,  options, account, logout ],
    top_dash_instructor:    [ jwt_test, home, dashboard, notifications,  options, account, logout, login ],

};