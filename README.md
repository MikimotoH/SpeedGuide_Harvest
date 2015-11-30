# SpeedGuide Harvest
Harvest Router information on SpeedGuide

## How to use Firefox Inspector Tool to get Unique CSS Selector and CSS Selectors of all Items 

[![How to use Firefox Inspector Tool to get Unique CSS Selector and CSS Selectors of all Items ](http://img.youtube.com/vi/IetlknUBivs/0.jpg)](https://www.youtube.com/watch?v=IetlknUBivs "How to use Firefox Inspector Tool to get Unique CSS Selector and CSS Selectors of all Items ")

Step 1. pressing "Ctrl-Shift-I" to open "Inspector Tool" in Firefox.
Step 2. click "Pick an element from the page" (top-left corner of the inspector pane)
Step 3. click on the item you want to enumerate
Step 4. on the right most of the CSS Pane, right click, then select "Copy Unique CSS Selector"
Step 5. on the Web Console, paste the CSS Selector
Step 6. use JQuery "$('css-selector')" to examine whether the element shows in the web console output (if it is inside an IFRAME, the web element won't show)
Step 7. because we want to enumerate all of the items, we check the parent element's tag name and class ('em.router'), we insert the parent's CSS before the item.


