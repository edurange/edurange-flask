

import React from 'react';

import './Account.css';
import ChangeEmailForm from '../../../../../../templates/accountmgmt/components/email-form/ChangeEmailForm';

function Account () {
    return (
        <div>
            <div className='newdash-content-placard' >Account</div>
            <ChangeEmailForm/>
        </div>
    );
}

export default Account;


