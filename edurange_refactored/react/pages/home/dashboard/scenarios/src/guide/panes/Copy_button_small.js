import React, { useContext } from 'react';
import edurange_icons from '../../../../../../../modules/ui/edurangeIcons';
import { HomeRouterContext } from '../../../../../src/Home_router';
import copyToClipboard from '../../../../../../../modules/utils/copyToClipboard';
import './Copy_button_small.css';

function Copy_button_small({ thingToCopy }) {

    const { clipboard_state, set_clipboard_state } = useContext(HomeRouterContext);

    function handle_copyClick(textToCopy) {
        set_clipboard_state(textToCopy);
        copyToClipboard(textToCopy);
    };

    function clipboardOrCheckmark(stringToCopy) {
        if (clipboard_state === stringToCopy) {
            return (
                <div className='copyCheck-frame' onClick={() => handle_copyClick(thingToCopy)}>
                    <div className='copyCheck-icon'>{edurange_icons.checkmark}</div>
                </div>
            );
        }
        else {
            return (
                <div className='copyButton-frame' onClick={() => handle_copyClick(thingToCopy)}>
                    <div className='copyButton-icon'>{edurange_icons.clipboard_copy}</div>
                </div>
            );
        };
    };
    return (
        <>
            {clipboardOrCheckmark(thingToCopy)}
        </>
    );
};
export default Copy_button_small;

