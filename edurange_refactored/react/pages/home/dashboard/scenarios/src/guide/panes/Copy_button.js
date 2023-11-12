import React, { useContext } from 'react';
import edurange_icons from '../../../../../../../modules/ui/edurangeIcons';
import { HomeRouterContext } from '../../../../../src/Home_router';
import copyToClipboard from '../../../../../../../modules/utils/copyToClipboard';
import './Copy_button.css';

function Copy_button({thingToCopy}) {

    const { clipboard_state, set_clipboard_state } = useContext(HomeRouterContext);

    function handle_copyClick(textToCopy){
        set_clipboard_state(textToCopy);
        copyToClipboard(textToCopy);
    };

    function clipboardOrCheckmark(stringToCopy) {
        if (clipboard_state === stringToCopy) {
            return (
                <div className='green-checkmark-content' >
                    <div className='green-checkmark-icon'>{edurange_icons.checkmark}</div>
                </div>
            );
        }
        else {
            return (
                <div className='ssh-copyButton-content' >
                    <div className='sshcard-icon'>{edurange_icons.clipboard_copy}</div>
                    <div className='sshcard-icon-label'>COPY</div>
                </div>
            );
        };
    };

    return (
        <div className='copyColumn-button-frame' onClick={() => handle_copyClick(thingToCopy)}>
            {clipboardOrCheckmark(thingToCopy)}
        </div>
    );
};
export default Copy_button;

