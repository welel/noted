/* Functions for comments block on note details. */

/**
*   Expand a list with children comments for root comment.
*   
*   Args:
*       @param {string} childrenDivId: `id` of a root `div` for all children comments,
*           example: childrenComments7
*       @param {string} arrowId: `id` of a `span` with an arrow unicode symbol inside,
*            example: arrow7
*
*   The function is called on click on an arrow symbol of a root comment, and it expands
*   children comments below the root. Also, it changes the arrow symbol which changes
*   direction of the arrow.
*/
function expandChildren(childrenDivId, arrowId) {
    var children = document.getElementById(childrenDivId);
    var arrow = document.getElementById(arrowId);
    if (children.hidden) {
        children.hidden = false;
        arrow.innerText = '\u25B4';
    } else {
        children.hidden = true;
        arrow.innerText = '\u25BE';
    }
}


/**
*   Expand a comment form by clicking `reply` button.
*   
*   Args:
*       @param {number} parentId: `id` of a root comment of a replying comment,
*           it uses for prepopulation of `parent` field of a ``CommentForm``. 
*       @param {number} commentId: `id` of a replying comment
*
*   The function expands a comment form for replying to another comment.
*/
function openCommentForm(parentId, commentId) {
    // Get csrf token from the main comment form
    var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0]['defaultValue'];
    // If a replying comment form already opened, close it
    if (document.contains(document.getElementById('commentForm'))) {
        document.getElementById('commentForm').remove();
    }
    // Add a form below of a replying comment
    var commentLastElement = document.getElementById(commentId);
    commentLastElement.insertAdjacentHTML('afterend',
        '<form id="commentForm" class="m-auto" method="post"> \
        <p> \
            <select name="parent" class="d-none" required="" id="id_parent"> \
                <option value="' + parentId + '" selected="' + parentId + '"></option> \
            </select> \
        </p> \
            <p> <lt-mirror contenteditable="false" style="display: none;"><lt-highlighter contenteditable="false" style="display: none;"><lt-div spellcheck="false" class="lt-highlighter__wrapper" style="width: 694px !important; height: 60px !important; transform: none !important; transform-origin: 348px 31px !important; zoom: 1 !important; margin-top: 1px !important; margin-left: 1px !important;"><lt-div class="lt-highlighter__scroll-element" style="top: 0px !important; left: 0px !important; width: 694px !important; height: 60px !important;"></lt-div></lt-div></lt-highlighter><lt-div spellcheck="false" class="lt-mirror__wrapper notranslate" data-lt-scroll-top="0" data-lt-scroll-left="0" data-lt-scroll-top-scaled="0" data-lt-scroll-left-scaled="0" data-lt-scroll-top-scaled-and-zoomed="0" data-lt-scroll-left-scaled-and-zoomed="0" style="border: 1px solid rgb(206, 212, 218) !important; border-radius: 4px !important; direction: ltr !important; font: 400 16px / 1.5 system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot; !important; font-feature-settings: normal !important; font-kerning: auto !important; font-synthesis: weight style small-caps !important; hyphens: manual !important; letter-spacing: normal !important; line-break: auto !important; margin: 0px !important; padding: 6px 12px !important; text-align: start !important; text-decoration: none solid rgb(33, 37, 41) !important; text-indent: 0px !important; text-rendering: auto !important; text-transform: none !important; transform: none !important; transform-origin: 348px 31px !important; unicode-bidi: normal !important; white-space: pre-wrap !important; word-spacing: 0px !important; overflow-wrap: break-word !important; writing-mode: horizontal-tb !important; zoom: 1 !important; -webkit-locale: &quot;en&quot; !important; -webkit-rtl-ordering: logical !important; width: 670px !important; height: 48px !important;"><lt-div class="lt-mirror__canvas" style="margin-top: 0px !important; margin-left: 0px !important; width: 670px !important; height: 48px !important;"></lt-div></lt-div></lt-mirror><textarea name="content" cols="40" rows="2" class="form-control shadow-none" placeholder="Add a public comment..." maxlength="2000" required="" id="id_content" data-lt-tmp-id="lt-883410" spellcheck="false" data-gramm="false"></textarea></p> \
            <input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"> \
            <button type="submit" class="btn btn-primary btn-block float-end px-4 shadow-none">Post</button> \
            <button type="button" class="btn btn-secondary btn-block float-end px-4 mx-2 shadow-none" onclick="closeCommentForm()">Cancel</button> \
        </form>'
    );
}

/**
 *  Close a replying comment form on `Cancel` button click.
 */
function closeCommentForm() {
    document.getElementById('commentForm').remove();
}
