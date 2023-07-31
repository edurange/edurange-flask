
import React from "react";
import { edurange_icons } from "../../edurange_icons";

export const NavData_logged_in = [
    

{
    title: "Home",
    icon: edurange_icons.home_icon, 
    link: 1,
    path: `/home_sister`
},
{
    title: "Dashboard",
    icon: edurange_icons.computer_monitor_icon, 
    link: 2,
    path: `/dashboard/`
},
{
    title: "Scenarios",
    icon: edurange_icons.chess_knight_icon, 
    link: 3,
    path: `/dashboard/scenarios`
},
{
    title: "Notifications",
    icon: edurange_icons.bell_icon, 
    link: 4,
    path: `/dashboard/notification_history`
},
{
    title: "Docs",
    icon: edurange_icons.book_icon, 
    link: 5,
    path: `/home_sister/about`
},
{
    title: "Options",
    icon: edurange_icons.gear_icon, 
    link: 6,
    path: `/home_sister/options`
},
{
    title: "Account",
    icon: edurange_icons.user_icon, 
    link: 7,
    path: `/dashboard/accountmgmt`
},
{
    title: "Logout",
    icon: edurange_icons.user_x_icon, 
    link: 7,
    path: `/home_sister/logout`
},
]

export const NavData_logged_out = [

    {
        title: "Home",
        icon: edurange_icons.home_icon, 
        link: 1,
        path: `/home_sister`
    },
    {
        title: "Docs",
        icon: edurange_icons.book_icon, 
        link: 5,
        path: `/home_sister/about`
    },
    {
        title: "Options",
        icon: edurange_icons.gear_icon, 
        link: 6,
        path: `/home_sister/options`
    },
    {
        title: "Login",
        icon: edurange_icons.user_check_icon, 
        link: 7,
        path: `/home_sister/login`
    },
    ]