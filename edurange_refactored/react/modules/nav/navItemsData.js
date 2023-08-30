
// these are used by some menus to define what their label, icon, and link path should be
// at the bottom, arrays define which items should be displayed in which contexts
// you can simply add some more and use them as you wish

import { edurange_icons } from "../ui/edurangeIcons";

const home_nav = {
    title: "Home",
    icon: edurange_icons.home_icon,
    path: `/edurange3`
}
const login_nav = {
    title: "Login",
    icon: edurange_icons.user_check_icon,
    path: `/edurange3/login`
}
const logout_nav = {
    title: "Logout",
    icon: edurange_icons.user_x_icon,
    path: `/edurange3/dashboard/logout`
}
const options_nav = {
    title: "Options",
    icon: edurange_icons.gear_icon,
    path: `/edurange3/options`
}
const admin_nav = {
    title: "Admin",
    icon: edurange_icons.gear_icon,
    path: `/edurange3/admin`
}
const instructor_nav = {
    title: "Instructor",
    icon: edurange_icons.gear_icon,
    path: `/edurange3/instructor`
}
const info_home_nav = {
    title: "Info",
    icon: edurange_icons.book_icon,
    path: `/edurange3/info`
}
const docs_nav = {
    title: "Docs",
    icon: edurange_icons.book_icon,
    path: `/edurange3/info/docs`
}
const about_nav = {
    title: "About",
    icon: edurange_icons.book_icon,
    path: `/edurange3/info/about`
}
const contact_nav = {
    title: "Contact",
    icon: edurange_icons.book_icon,
    path: `/edurange3/info/contact`
}
const help_nav = {
    title: "Help",
    icon: edurange_icons.questionmark_icon,
    path: `/edurange3/info/help`
}
const dashboard_nav = {
    title: "Dashboard",
    icon: edurange_icons.computer_monitor_icon,
    path: `/edurange3/dashboard`
}
const account_nav = {
    title: "Account",
    icon: edurange_icons.account_icon,
    path: `/edurange3/dashboard/account`
}
const scenarios_nav = {
    title: "Scenarios",
    icon: edurange_icons.chess_knight_icon,
    path: `/edurange3/dashboard/scenarios`
}
const notifications_nav = {
    title: "Notifications",
    icon: edurange_icons.bell_icon,
    path: `/edurange3/dashboard/notifications`
}
const ssh_nav = {
    title: "Connect via SSH",
    icon: edurange_icons.terminal_prompt_icon,
    path: `/edurange3/dashboard/ssh`
}
const devtable_nav = {
    title: "Instructor Data:",
    icon: edurange_icons.eye_icon,
    path: `/edurange3/dashboard/admin/devtable`
}
const instructor_userGroups_nav = {
    title: "Student Groups",
    icon: edurange_icons.userGroup_icon,
    path: `/edurange3/dashboard/userGroups`
}
const instructor_scenarioGroups_nav = {
    title: "Scenario Groups",
    icon: edurange_icons.scenarioGroup_icon,
    path: `/edurange3/dashboard/scenarioGroups`
}
const instructor_users_nav = {
    title: "Students",
    icon: edurange_icons.user_icon,
    path: `/edurange3/dashboard/users`
};
const jwt_test_nav = {
    title: "jwt_test",
    icon: edurange_icons.key_icon,
    path: `/edurange3/dashboard/jwt_test`
};
const themes_nav = {
    title: "Themes",
    icon: edurange_icons.palette_icon,
    path: `/edurange3/options/themes`
};
const accessibility_nav = {
    title: "Accessibility",
    icon: edurange_icons.accessibility_icon,
    path: `/edurange3/options/accessibility`
};

export const SideNav_student_logged_in =    [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav, login_nav ]
export const SideNav_instructor_logged_in = [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav, login_nav ]
export const SideNav_admin_logged_in =      [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav, login_nav ]
export const SideNav_logged_out =           [ jwt_test_nav, home_nav, docs_nav, options_nav,login_nav ]

export const TopNav_student_logged_in =    [ jwt_test_nav, home_nav,ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav, login_nav ]
export const TopNav_instructor_logged_in = [ jwt_test_nav,home_nav,ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav , login_nav]
export const TopNav_admin_logged_in =      [ jwt_test_nav,home_nav,ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav , login_nav]
export const TopNav_logged_out =           [  jwt_test_nav, home_nav, docs_nav, options_nav, login_nav ]

export const DashSideNav_student_logged_in =    [ jwt_test_nav, dashboard_nav, scenarios_nav, notifications_nav, ssh_nav, options_nav,  account_nav, logout_nav ]
export const DashSideNav_instructor_logged_in = [ jwt_test_nav, dashboard_nav, devtable_nav, instructor_users_nav, scenarios_nav, notifications_nav,  ssh_nav, options_nav, account_nav,  logout_nav, login_nav ]
export const DashSideNav_admin_logged_in =      [ jwt_test_nav, dashboard_nav, devtable_nav, instructor_users_nav, scenarios_nav, notifications_nav,  ssh_nav, options_nav, account_nav,  logout_nav, login_nav ]
export const DashSideNav_logged_out =           [ jwt_test_nav, home_nav, docs_nav, options_nav,login_nav ]

export const DashContextNav_student_logged_in =    [ dashboard_nav, scenarios_nav, notifications_nav, ssh_nav, options_nav,  account_nav, login_nav,logout_nav ]
export const DashContextNav_instructor_logged_in = [ dashboard_nav, instructor_users_nav, scenarios_nav, notifications_nav,  ssh_nav, options_nav, account_nav,  login_nav,logout_nav, devtable_nav ]
export const DashContextNav_admin_logged_in =      [ dashboard_nav, instructor_users_nav, scenarios_nav, notifications_nav,  ssh_nav, options_nav, account_nav,  login_nav,logout_nav, devtable_nav ]
export const DashContextNav_logged_out =           [ jwt_test_nav, home_nav, docs_nav, options_nav,login_nav ]

export const Options_SideNav =           [ accessibility_nav, themes_nav ]

