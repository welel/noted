// input
const sourceInputField = document.getElementById('id_source');
const sourceTypeInputField = document.getElementById('id_source_type');
const sourceLinkInputField = document.getElementById('id_source_link');
const sourceDescriptionInputField = document.getElementById('id_source_description');

// buttons
const openSourceModalButton = document.getElementById('add-source-btn');
const sourceAddButton = document.getElementById('add-source-modal');
const sourceCloseButton = document.getElementById('close-source-modal');
const sourceRemoveButton = document.getElementById('remove-source-btn');

// elements
const selectedSourceHiddenElement = document.getElementById('selected-source-hidden');
const selectedSourceElement = document.getElementById('selected-source');
const sourcesOutputElement = document.getElementById('sources-output');
const sourcesListElement = document.getElementById('sourses-list');

// URL
const get_sources_url = document.getElementById('get-sources-url').innerText;


/**
 * Get existing sources in the database and output to a HTML element.
 * The source title input element as a query requests sources via ajax. 
 */
sourceInputField.oninput = (event) => {
    if (sourceInputField.value.length > 3) {
        $.ajax({
            type: 'GET',
            data: {'query': sourceInputField.value},
            url: get_sources_url,
            headers: {"X-Requested-With": "XMLHttpRequest"},
            success: function(response) {
                
                let output = [];
                for (source_id in response.data) {
                    let id = response.data[source_id].id
                    let source_type_code = response.data[source_id].type[0]
                    let source_type = response.data[source_id].type[1]
                    let title = response.data[source_id].title
                    let link = response.data[source_id].link
                    let description = response.data[source_id].description
                    output.push(`<tr class="source-table-row"> \
                        <td id="source-type-${id}" code="${source_type_code}">${source_type}</td> \
                        <td id="source-${id}">${title}</td> \
                        <td><button type="button" class="btn btn-sm btn-success rounded-pill" onclick="select(${id});">Select</button></td> \
                        <span id="source-link-${id}" hidden>${link}</span> \
                        <span id="source-description-${id}" hidden>${description}</span> \
                        </tr>`
                    );
                    sourcesOutputElement.innerHTML = output.join('');
                    sourcesListElement.hidden = false;
                }
                if (response.data.length == 0) {
                    sourcesListElement.hidden = true;
                }
            },
            error: function (response) {
                console.log('NO');
            },
            timeout: 2400
        });
    }
}


// Display a source in the note form.
function showSource (event) {
    if (sourceInputField.value.length != 0) {
        selectedSourceElement.innerHTML = '<span class="badge text-bg-success rounded-pill">' +
                                            sourceTypeInputField.selectedOptions[0].innerText +
                                            '</span><a href="#" class="ms-2 fw-bold text-dark text-decoration-none" data-bs-toggle="modal" data-bs-target="#add-source-modal">' +
                                            sourceInputField.value + '</a>';
        selectedSourceHiddenElement.hidden = false;
        openSourceModalButton.hidden = true;
    }
}


sourceAddButton.onclick = showSource;


// Remove a source from the note form.
sourceRemoveButton.onclick = (event) => {
    selectedSourceHiddenElement.hidden = true;
    openSourceModalButton.hidden = false;
    sourceInputField.value = '';
    sourceLinkInputField.value = '';
    sourceDescriptionInputField.value = '';
}


// Select a source to input.
function select(val) {
    sourceTypeInputField.selectedIndex = document.getElementById('source-type-' + val).getAttribute('code');
    sourceInputField.value = document.getElementById('source-' + val).innerText;
    sourceLinkInputField.value = document.getElementById('source-link-' + val).innerText;
    sourceDescriptionInputField.value = document.getElementById('source-description-' + val).innerText;
}

window.onload = function(){
    if (sourceInputField.value.length != 0) {
        showSource(event);
    }
};
