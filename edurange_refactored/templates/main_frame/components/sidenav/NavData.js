
import React from "react";
// import React from 'react';

import { FaHouseChimney } from "react-icons/fa6";
import { FaAddressCard } from "react-icons/fa6";
import { FaFileLines } from "react-icons/fa6";
import { FaChessKnight } from "react-icons/fa6";
import { FaDisplay } from "react-icons/fa6";
import { FaCircleUser } from "react-icons/fa6";
import { FaUserXmark } from "react-icons/fa6";

// import { FaBell } from "react-icons/fa6";
// import { FaChartBar } from "react-icons/fa6";
// import { FaCheck } from "react-icons/fa6";
// import { FaChevronRight } from "react-icons/fa6";
// import { FaChevronLeft } from "react-icons/fa6";
// import { FaChildReaching } from "react-icons/fa6";
// import { FaCircleXmark } from "react-icons/fa6";
// import { FaClipboardCheck } from "react-icons/fa6";
// import { FaCommentDots } from "react-icons/fa6";
// import { FaFolderTree } from "react-icons/fa6";
// import { FaGear } from "react-icons/fa6";
// import { FaDungeon } from "react-icons/fa6";
// import { FaPencil } from "react-icons/fa6";
// import { FaRegCopy } from "react-icons/fa6";
// import { FaToggleOff } from "react-icons/fa6";
// import { FaToggleOn } from "react-icons/fa6";

// const bell_icon = <FontAwesomeIcon icon={FaBell} />
// const chart_icon = <FontAwesomeIcon icon={FaChartBar} />
// const leftChevron_icon = <FontAwesomeIcon icon={FaChevronLeft} />
// const rightChevron_icon = <FontAwesomeIcon icon={FaChevronRight} />
// const check_icon = <FontAwesomeIcon icon={FaCheck} />
// const accessibility_icon = <FontAwesomeIcon icon={FaChildReaching} />
// const circle_x_icon = <FontAwesomeIcon icon={FaCircleXmark} />
// const clipboard_check_icon = <FontAwesomeIcon icon={FaClipboardCheck} />
// const chat_icon = <FontAwesomeIcon icon={FaCommentDots} />
// const folder_tree_icon = <FontAwesomeIcon icon={FaFolderTree} />
// const pencil_icon = <FontAwesomeIcon icon={FaPencil} />
// const gear_icon = <FontAwesomeIcon icon={FaGear} />
// const dungeon_icon = <FontAwesomeIcon icon={FaDungeon} />
// const carbon_copy_icon = <FontAwesomeIcon icon={FaRegCopy} />
// const toggle_off_icon = <FontAwesomeIcon icon={FaToggleOff} />
// const toggle_on_icon = <FontAwesomeIcon icon={FaToggleOn} />
// const chess_knight_icon = <FontAwesomeIcon icon={FaChessKnight} />

const home_icon = <FaHouseChimney />
const docs_icon = <FaFileLines />
const identity_icon = <FaAddressCard />
const chess_knight_icon = <FaChessKnight />
const user_icon = <FaCircleUser />
const user_x_icon = <FaUserXmark />
const computer_monitor_icon = <FaDisplay />

export const NavData = [

{
    title: "Home",
    icon: home_icon, 
    link: "/home_sister"
},
{
    title: "Docs",
    icon: docs_icon, 
    link: "/home_sister"
},
{
    title: "Scenarios",
    icon: chess_knight_icon, 
    link: "/home_sister"
},
{
    title: "Dashbar",
    icon: computer_monitor_icon, 
    link: "/home_sister"
},
{
    title: "Account",
    icon: user_icon, 
    link: "/home_sister"
},
{
    title: "Login",
    icon: identity_icon, 
    link: "/home_sister"
},
{
    title: "Logout",
    icon: user_x_icon, 
    link: "/home_sister"
},
]