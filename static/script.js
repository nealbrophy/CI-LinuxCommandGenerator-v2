function copyToClipboard(inputText) {
    let textArea = document.createElement("textarea");
    textArea.value = inputText;
    textArea.style.position = "fixed";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        let successful = document.execCommand("copy");
        let msg = successful ? "successful" : "unsuccessful";
    } catch (err) {
        console.log("Copy failed", err);
    }
    document.body.removeChild(textArea);
}


// add click listener to copy button
let copyCommand = document.getElementsByClassName('command_to_copy');
for (let i = 0; i < copyCommand.length; i++) {
    copyCommand[i].addEventListener("click", function () {
        copyToClipboard(document.getElementById(this.id).innerText)
    })
}
