// Color theme toggle
const lightThemeUrl = document.getElementById('css-light-theme-url'); 
const darkThemeUrl = document.getElementById('css-dark-theme-url');
const themeBtn = document.getElementById('theme-btn');
const themeBtn2 = document.getElementById('theme-btn-2');
const styleLink = document.getElementById('color-theme');
themeBtn.onclick = (event) => {
    if (styleLink.href == lightThemeUrl.href) {
        styleLink.href = darkThemeUrl.href;
        themeBtn.lastElementChild.innerText = gettext('Light theme');
        themeBtn2.lastElementChild.innerText = gettext('Light theme');
        $(".theme-btn-cl").attr("class", "bi bi-brightness-high px-2 theme-btn-cl");
        localStorage.setItem('theme', darkThemeUrl.href);
    } else {
        styleLink.href = lightThemeUrl.href;
        themeBtn.lastElementChild.innerText = gettext('Dark theme');
        themeBtn2.lastElementChild.innerText = gettext('Dark theme');
        $(".theme-btn-cl").attr("class", "bi bi-brightness-high px-2 theme-btn-cl");
        localStorage.setItem('theme', lightThemeUrl.href);
    }
}
themeBtn2.onclick = themeBtn.onclick;
const theme = localStorage.getItem('theme');
if (theme == darkThemeUrl.href) {
    styleLink.href = darkThemeUrl.href;
    themeBtn.lastElementChild.innerText = gettext('Light theme');
    themeBtn2.lastElementChild.innerText = gettext('Light theme');
    $(".theme-btn-cl").attr("class", "bi bi-brightness-high px-2 theme-btn-cl");
}
