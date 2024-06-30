/*
* BIA601 - Dr.Bassel Alkhatib
* hassan_125191
* hebatullah_153525
* mhd_hussam_109817
* mohamad_108528
* samar_115286
* */

function handleFileSelect() {
    var fileSelector = document.getElementById("fileSelector");
    var chooseButton = document.getElementById("chooseButton");

    if (fileSelector.value === "upload") {
        chooseButton.style.display = "block";
    } else {
        chooseButton.style.display = "none";
    }
}

let fileContents = {};  // JavaScript object to store file contents
let filesSelected = false;

function handleFileContent() {
    var fileInput = document.getElementById("fileInput");

    // Check if files are selected
    if (fileInput.files.length > 0) {
        filesSelected = true;
        const docsSmall = document.getElementById("docsSmall");
        docsSmall.style.display = "none";
        // Loop through selected files
        for (var i = 0; i < fileInput.files.length; i++) {
            var file = fileInput.files[i];

            console.log("File selected:", file.name);

            // Read the content of each .docx file using mammoth.js and store in the array
            readDocxContent(file);
        }
    } else {
        filesSelected = false;
    }
}

function readDocxContent(file) {
    var reader = new FileReader();

    reader.onload = function (e) {
        var arrayBuffer = e.target.result;

        // Use mammoth.js to convert .docx to HTML
        mammoth.extractRawText({arrayBuffer: arrayBuffer})
            .then(function (result) {
                var fileName = file.name;

                // Replace newline characters with an empty string
                fileContents[fileName] = result.value.replace(/\n+/g, ' ');
            })
            .catch(function (error) {
                console.error("Error extracting text:", error);
            });
    };

    reader.readAsArrayBuffer(file);
    // console.log(fileContents);
}


$(document).ready(function () {
    // When the search  button gets pressed
    $(".queries").click(function () {
        let selectedLanguage = document.getElementById('languageSelect');
        selectedLanguage = selectedLanguage.value;

        const fileSelector = document.getElementById("fileSelector");
        const fileSelectorValue = fileSelector.value;

        console.log(fileContents);

        let formData = new FormData();

        formData.append('language', selectedLanguage);
        formData.append('documents', JSON.stringify(fileContents));

        if (fileSelectorValue === "use_predefined") {
            if (selectedLanguage === "arabic")
                window.location.href = "/search/1/";
            else
                window.location.href = "/search/2";
        } else if (!filesSelected) {
            const docsSmall = document.getElementById("docsSmall");
            docsSmall.style.display = "block";
        } else {
            $.ajax({
                url: '',  // Specify your URL
                type: 'POST',
                data: formData,
                processData: false,  // Prevent jQuery from processing the data
                contentType: false,  // Prevent jQuery from setting the Content-Type header
                success: function (response) {
                    console.log(response);
                    if (response.redirect_url) {
                        // Redirect to the new URL
                        console.log('HELLO', response.identifier);

                        window.location.href = response.redirect_url;
                    } else {
                        // Handle other aspects of the response as needed
                        console.log(response);
                    }
                    // Handle the response as needed
                    console.log(response);
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    $("#homeButton").click(function () {
        window.location.href = "/main";
    });

    $(".search").click(function () {
        let selectedRetrievalModel = document.getElementById('retrievalModelSelect');
        selectedRetrievalModel = selectedRetrievalModel.value;

        let query = document.getElementById('query');
        query = query.value.trim();

        const querySmall = document.getElementById('querySmall');
        console.log(query);
        if (query !== '') {
            querySmall.style.display = "none";
            let formData = new FormData();

            formData.append('retrieval_model', selectedRetrievalModel);
            formData.append('query', query);

            const docsTabs = document.getElementById("docsTabs");

            $.ajax({
                url: '',  // Specify your URL
                type: 'POST',
                data: formData,
                processData: false,  // Prevent jQuery from processing the data
                contentType: false,  // Prevent jQuery from setting the Content-Type header
                success: function (response) {
                    console.log(response);
                    output.innerHTML = "";
                    console.log(response.docs_result.length);
                    if (response.docs_result.length) { // Check the length of response.docs
                        var documents = response.docs_result;
                        // Loop through the documents and create HTML elements
                        let docsTabsHTML = `<ul class="nav nav-tabs" id="docsTab" role="tablist">`;
                        let docsTabsContentHTML = `<div class="tab-content" id="docsTabContent">`;

                        documents.forEach(function (document, i) {
                            let uniqueId = `doc${i + 1}`;  // Ensure unique ID

                            docsTabsHTML += `
        <li class="nav-item" role="presentation">
            <button
                class="nav-link ${i === 0 ? 'active' : ''}"
                id="${uniqueId}-tab"
                data-bs-toggle="tab"
                data-bs-target="#${uniqueId}"
                type="button"
                role="tab"
                aria-controls="${uniqueId}"
                aria-selected="${i === 0 ? 'true' : 'false'}"
            >
                ${document.doc_name}
            </button>
        </li>
    `;

                            docsTabsContentHTML += `
        <div
            class="tab-pane fade ${i === 0 ? 'show active' : ''}"
            id="${uniqueId}"
            role="tabpanel"
            aria-labelledby="${uniqueId}-tab"
        >
                <span style="color: dodgerblue">Ratio of similarity between query and document is ${document.doc_sim}</span>
                <br>
                <br>
                        ${document.doc_content}
                    </div>
                `;
                        });

                        docsTabsHTML += `</ul>`;
                        docsTabsContentHTML += '</div>';
                        docsTabsHTML += docsTabsContentHTML;
                        docsTabs.innerHTML = docsTabsHTML;
                    } else {
                                                const noMatching = `
                            <div class="text-center">
                                <h3>No matching found</h3>
                            </div>
                        `;
                        var allDocuments = response.docs;
                        const outputArray = Object.entries(allDocuments).map(([doc_name, doc_content]) => ({
                            doc_name,
                            doc_content
                        }));
                        outputArray.pop();
                                                let docsTabsHTML = `<ul class="nav nav-tabs" id="docsTab" role="tablist">`;
                        let docsTabsContentHTML = `<div class="tab-content" id="docsTabContent">`;

                        outputArray.forEach(function (document, i) {
                            let uniqueId = `doc${i + 1}`;  // Ensure unique ID

                            docsTabsHTML += `
        <li class="nav-item" role="presentation">
            <button
                class="nav-link ${i === 0 ? 'active' : ''}"
                id="${uniqueId}-tab"
                data-bs-toggle="tab"
                data-bs-target="#${uniqueId}"
                type="button"
                role="tab"
                aria-controls="${uniqueId}"
                aria-selected="${i === 0 ? 'true' : 'false'}"
            >
                ${document.doc_name}
            </button>
        </li>
    `;

                            docsTabsContentHTML += `
        <div
            class="tab-pane fade ${i === 0 ? 'show active' : ''}"
            id="${uniqueId}"
            role="tabpanel"
            aria-labelledby="${uniqueId}-tab"
        >
                        ${document.doc_content}
                    </div>
                `;
                        });

                        docsTabsHTML += `</ul>`;
                        docsTabsContentHTML += '</div>';
                        docsTabsHTML += docsTabsContentHTML;
                        docsTabs.innerHTML = noMatching + docsTabsHTML;
                        console.log(outputArray);

                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        } else {
            querySmall.style.display = "block";
        }
    });
});


// ====================
// Add or remove loading class on element depending on Ajax request status
$(document).on({
    ajaxStart: function () {
        $("#res-card").hide();
        $("#loading").show();
        console.log('Query started');
    },
    ajaxStop: function () {
        $("#res-card").show();
        $("#loading").hide();
        console.log('Query ended');
    }
});


// ====================
// Configuring the popup dialogue for the About button
// Get the modal
const modal = document.getElementById("aboutModal");

// Get the button that opens the modal
const btn = document.getElementById("aboutButton");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside the modal, or presses the escape button, close it
window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
    $(document).keyup(function (e) {
        if (e.key === "Escape") {
            modal.style.display = "none";
        }
    });
}

