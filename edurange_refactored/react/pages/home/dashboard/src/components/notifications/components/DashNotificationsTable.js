

import React from 'react';
import './DashNotifications.css';

function DashNotificationsTable(props) {
    
    return (
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
                    {/* Temporarily Disabled for Dev */}
                    {/* <tbody>{notifications_built}</tbody> */}
                </table>
            </div>
        </div>
    );
};
export default DashNotificationsTable;