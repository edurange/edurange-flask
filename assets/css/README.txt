


'pucs.css' serves as the NEW 'style.css' file for "edurange-React".

Currently, both are being packed up by webpack and applied,
but pucs.css is loaded afterward, and the first thing it does is reset all styles,
so any styles that are defined in `pucs.css` will be from a fresh start inside the new UI,
and many styles that were previously available with 'style.css' will no longer be defined.

This is to cut down on css element/class styling conflicts and other hidden and confusing css issues that
tend to occur when importing large numbers of predefined styles (as we are with packing up bootstrap, 
fontAwesome, and style.css into one large .css file with webPack).

TLDR: Both 'style.css' and 'pucs.css' represent the Project Unified Custom Styling (PUCS) 
which sits above bootstrap and fontAwesome styles and below component specific styling in terms
of style hierarchy (and reverse in terms of evaluation order), however, only 'style.css' applies to legacy,
and only 'pucs.css' applies to edurange-react.