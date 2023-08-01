
import { edurange_icons } from "../../edurange_icons";

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
const dashboard_nav = {
    title: "Dashboard",
    icon: edurange_icons.home_icon,
    path: `/home_sister/dashboard`
}
const account_nav = {
    title: "Account",
    icon: edurange_icons.user_icon,
    path: `/dashboard/account`
}
const scenarios_nav = {
    title: "Scenarios",
    icon: edurange_icons.chess_knight_icon,
    path: `/dashboard/scenarios`
}
const notifications_nav = {
    title: "Notifications",
    icon: edurange_icons.bell_icon,
    path: `/dashboard/notifications`
}






export const NavData_student_logged_in =    [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav ]
export const NavData_instructor_logged_in = [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav ]
export const NavData_admin_logged_in =      [ home_nav, dashboard_nav, scenarios_nav, notifications_nav, docs_nav, options_nav, account_nav, logout_nav ]
export const NavData_logged_out =           [ home_nav, docs_nav, options_nav, login_nav]

