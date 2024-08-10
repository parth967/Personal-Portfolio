// Dummy data for pages
let pages = [];

// Function to render pages list
function renderPages() {
    const pagesList = document.getElementById("pagesList");
    pagesList.innerHTML = "";
    pages.forEach(page => {
        const pageItem = document.createElement("div");
        pageItem.classList.add("page-item");
        pageItem.textContent = page.title;
        pageItem.addEventListener("click", () => {
            document.getElementById("pageTitle").value = page.title;
            document.getElementById("pageContent").value = page.content;
        });
        pagesList.appendChild(pageItem);
    });
}

renderPages();

document.getElementById("addHeaderBtn").addEventListener("click", () => {
    const contentTextArea = document.getElementById("pageContent");
    const currentPosition = contentTextArea.selectionStart;
    const headerText = prompt("Enter header text:");
    if (headerText !== null) {
        const currentContent = contentTextArea.value;
        const newContent = currentContent.slice(0, currentPosition) + `<h2>${headerText}</h2>` + currentContent.slice(currentPosition);
        contentTextArea.value = newContent;
    }
});

// Event listener for save button
document.getElementById("saveBtn").addEventListener("click", () => {
    const title = document.getElementById("pageTitle").value;
    const content = document.getElementById("pageContent").value;
    const newPage = { id: pages.length + 1, title, content };
    pages.push(newPage);
    renderPages();
});
