
import React from "react";

// import Icon Object references from the react-icon "font-awesome 6" library
// (import and use the variables from this file, rather than importing icons directly.  
// if you need more icons, import/add them from here!  https://react-icons.github.io/react-icons/

// usage example in React:  
//
//  import { edurange_icons } from "path/to/this/file/edurange_icons.js";
//  
//  MyComponent(){
//
//    return (
//      <div>{edurange_icons.bell_icon}</div>
//    );
//  } 
//  export default MyComponent;

import {
    FaHouseChimney,
    FaAddressCard,
    FaFileLines,
    FaChessKnight,
    FaDisplay,
    FaCircleUser,
    FaUserXmark,
    FaUserCheck,
    FaGear,
    FaBell,
    FaBook,
    FaUniversalAccess,
    FaCircleQuestion,
    FaBars,
    FaTerminal,
    FaEye
} from "react-icons/fa6";

// assign to specific vars to use appwide. (use these instead of importing directly)

export const edurange_icons = {
    accessibility_icon : <FaUniversalAccess/>,
    bell_icon : <FaBell/>,
    gear_icon : <FaGear/>,
    home_icon : <FaHouseChimney />,
    file_icon : <FaFileLines />,
    book_icon : <FaBook/>,
    identity_icon : <FaAddressCard />,
    chess_knight_icon : <FaChessKnight />,
    user_icon : <FaCircleUser />,
    user_x_icon : <FaUserXmark />,
    user_check_icon : <FaUserCheck />,
    computer_monitor_icon : <FaDisplay />,
    questionmark_icon : <FaCircleQuestion/>,
    hamburger_icon: <FaBars/>,
    terminal_prompt_icon: <FaTerminal/>,
    eye_icon: <FaEye/>
}

// good icons for web development that are not yet in use

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

// const chart_icon = <FontAwesomeIcon icon={FaChartBar} />
// const leftChevron_icon = <FontAwesomeIcon icon={FaChevronLeft} />
// const rightChevron_icon = <FontAwesomeIcon icon={FaChevronRight} />
// const check_icon = <FontAwesomeIcon icon={FaCheck} />
// const circle_x_icon = <FontAwesomeIcon icon={FaCircleXmark} />
// const clipboard_check_icon = <FontAwesomeIcon icon={FaClipboardCheck} />
// const chat_icon = <FontAwesomeIcon icon={FaCommentDots} />
// const folder_tree_icon = <FontAwesomeIcon icon={FaFolderTree} />
// const pencil_icon = <FontAwesomeIcon icon={FaPencil} />
// const dungeon_icon = <FontAwesomeIcon icon={FaDungeon} />
// const carbon_copy_icon = <FontAwesomeIcon icon={FaRegCopy} />
// const toggle_off_icon = <FontAwesomeIcon icon={FaToggleOff} />
// const toggle_on_icon = <FontAwesomeIcon icon={FaToggleOn} />