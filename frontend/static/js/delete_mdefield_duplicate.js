/*
    Markdown editor (SimpleMDE) duplicates because of crispy filter.
    This scripts removes duplicated editor.
 */

window.addEventListener("load", function(){
    var seen = {};
    $('.editor-toolbar').each(function() {
      var txt = $(this).text();
      if (seen[txt])
          $(this).remove();
      else
          seen[txt] = true;
    });
    var seen = {};
    $('.CodeMirror').each(function() {
      var txt = $(this).text();
      if (seen[txt])
          $(this).remove();
      else
          seen[txt] = true;
    });
});
