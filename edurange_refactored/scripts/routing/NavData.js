
import { edurange_icons } from "../../templates/main_frame/edurange_icons"

const home_nav = {
    title: "Home",
    icon: edurange_icons.home_icon,
    path: `/home_sister`
}
const login_nav = {
    title: "Login",
        icon: edurange_icons.user_check_icon,
        path: `/home_sister/login`
}
const logout_nav = {
    title: "Logout",
    icon: edurange_icons.user_x_icon,
    path: `/home_sister/logout`
}
const options_nav = {
    title: "Options",
    icon: edurange_icons.gear_icon,
    path: `/home_sister/options`
}
const admin_nav = {
    title: "Admin",
    icon: edurange_icons.gear_icon,
    path: `/home_sister/admin`
}
const instructor_nav = {
    title: "Instructor",
    icon: edurange_icons.gear_icon,
    path: `/home_sister/instructor`
}
const info_home_nav = {
    title: "Info",
    icon: edurange_icons.book_icon,
    path: `/home_sister/info`
}
const docs_nav = {
    title: "Docs",
    icon: edurange_icons.book_icon,
    path: `/home_sister/info/docs`
}
const about_nav = {
    title: "About",
    icon: edurange_icons.book_icon,
    path: `/home_sister/info/about`
}
const contact_nav = {
    title: "Contact",
    icon: edurange_icons.book_icon,
    path: `/home_sister/info/contact`
}
const help_nav = {
    title: "Help",
    icon: edurange_icons.questionmark_icon,
    path: `/home_sister/info/help`
}
const dashboard_nav = {
    title: "Dashboard",
    icon: edurange_icons.computer_monitor_icon,
    path: `/home_sister/dashboard`
}
const account_nav = {
    title: "Account",
    icon: edurange_icons.user_icon,
    path: `/home_sister/dashboard/account`
}
const scenarios_nav = {
    title: "Scenarios",
    icon: edurange_icons.chess_knight_icon,
    path: `/home_sister/dashboard/scenarios`
}
const notifications_nav = {
    title: "Notifications",
    icon: edurange_icons.bell_icon,
    path: `/home_sister/dashboard/notifications`
}
const ssh_nav = {
    title: "Connect via SSH",
    icon: edurange_icons.terminal_prompt_icon,
    path: `/home_sister/dashboard/ssh`
}
const devtable_nav = {
    title: "Dev Table",
    icon: edurange_icons.eye_icon,
    path: `/home_sister/dashboard/devtable`
}
const userGroups_nav = {
    title: "Dev Table",
    icon: edurange_icons.eye_icon,
    path: `/home_sister/dashboard/userGroups`
}
const scenarioGroups_nav = {
    title: "Dev Table",
    icon: edurange_icons.eye_icon,
    path: `/home_sister/dashboard/scenarioGroups`
}

export const SideNav_student_logged_in =    [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav ]
export const SideNav_instructor_logged_in = [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav ]
export const SideNav_admin_logged_in =      [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav , help_nav ]
export const SideNav_logged_out =           [ ]

export const TopNav_student_logged_in =    [ ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav ]
export const TopNav_instructor_logged_in = [ ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav ]
export const TopNav_admin_logged_in =      [ devtable_nav, ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav ]
export const TopNav_logged_out =           [ docs_nav, options_nav, login_nav ]

export const DashSideNav_student_logged_in =    [ dashboard_nav, scenarios_nav, notifications_nav, options_nav, account_nav, logout_nav ]
export const DashSideNav_instructor_logged_in = [ ssh_nav, dashboard_nav,userGroups_nav, scenarioGroups_nav, options_nav, account_nav, logout_nav ]
export const DashSideNav_admin_logged_in =      [ devtable_nav, ssh_nav, dashboard_nav, options_nav, account_nav, logout_nav ]
export const DashSideNav_logged_out =           [ login_nav ]

export const DashContextNav_student_logged_in =    [ dashboard_nav, scenarios_nav, notifications_nav, options_nav, account_nav, logout_nav ]
export const DashContextNav_instructor_logged_in = [ ssh_nav, dashboard_nav,userGroups_nav, scenarioGroups_nav, options_nav, account_nav, logout_nav ]
export const DashContextNav_admin_logged_in =      [ dashboard_nav,devtable_nav, ssh_nav, userGroups_nav, scenarioGroups_nav,  options_nav, account_nav, logout_nav ]
export const DashContextNav_logged_out =           [ login_nav ]


