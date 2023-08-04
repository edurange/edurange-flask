import React from 'react';
import './Notification.css';

function Notification(props) {

    // the follow code was written to generate the data with the legacy system
    // and has been disabled temporarily.
    // 
    // soon, the notifications array from the db will be handed down from the react entrypoint parent.

    // const notifs_obj = JSON.parse(props.notifications, (key, value) => {
    //     if (typeof value === 'number') {return value.toString();}
    //     return value;
    // });

    // function buildNotificationTable() {
    //     return Object.keys(notifs_obj).map((notifKey) => {
    //       const notif = notifs_obj[notifKey];
    //       return (
    //         <tr key={notif.id} className='pucs-table-base'>
    //           <td className='pucs-table-cell'>{notif.id}</td>
    //           <td className='pucs-table-cell'>{notif.date}</td>
    //           <td className='pucs-table-cell'>{notif.detail}</td>
    //         </tr>
    //       );
    //     });
    //   };
    // const notifications_built = buildNotificationTable();

    return (
        <div className='universal-page-parent'>
            <div className='universal-page-child'>
                <div className="notification-frame">
                    <div className='table-container'>
                        <table >
                            <caption>Table of Notification history</caption>
                            <thead className='pucs-table-head'>
                                <tr>
                                    <th className='pucs-table-cell'>Notification ID</th>
                                    <th className='pucs-table-cell'>Time Stamp</th>
                                    <th className='pucs-table-cell'>Message</th>
                                </tr>
                            </thead>
                            Temporarily Disabled for Dev
                            {/* <tbody>{notifications_built}</tbody> */}
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Notification;
