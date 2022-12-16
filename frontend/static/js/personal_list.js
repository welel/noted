const homeTab = document.getElementById('pills-home-tab');
const bookmarkTab = document.getElementById('pills-bookmarks-tab');
const pillsHome = document.getElementById('pills-home');
const pillsBookmarks = document.getElementById('pills-bookmarks');

// Set bookmark tab on `?bookmark=open` get parameter
document.addEventListener('DOMContentLoaded', function(){
    let bookmark = findGetParameter("bookmark");
    if (bookmark == 'open') { 
        homeTab.setAttribute("class", "nav-link tablink text-secondary");
        pillsHome.setAttribute("class", "tab-pane fade");
        bookmarkTab.setAttribute("class", "nav-link tablink text-secondary active");
        pillsBookmarks.setAttribute("class", "tab-pane fade active show");
    }
});
