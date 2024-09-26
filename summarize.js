javascript:(function() {

    if (document.getElementById('custom-movable-window')) return;

    const movableWindow = document.createElement('div');
    movableWindow.id = 'custom-movable-window';
    movableWindow.style.position = 'fixed';
    movableWindow.style.top = '50px';
    movableWindow.style.left = '50px';
    movableWindow.style.width = '400px';
    movableWindow.style.height = '300px';
    movableWindow.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    movableWindow.style.color = 'white';
    movableWindow.style.border = '1px solid #666';
    movableWindow.style.resize = 'both';
    movableWindow.style.overflow = 'auto';
    movableWindow.style.zIndex = '10000';
    movableWindow.style.padding = '10px';
    movableWindow.style.boxSizing = 'border-box';
    movableWindow.style.cursor = 'default';

    const textArea = document.createElement('div');
    textArea.style.width = '100%';
    textArea.style.height = '100%';
    textArea.style.overflowY = 'auto';
    textArea.fontSize = '1.3vh';
    textArea.style.whiteSpace = 'pre-wrap';
    textArea.contentEditable = true;
    textArea.style.outline = 'none';
    textArea.id = "text-text-area-1234";

    const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.setAttribute("width", "24");
    svgElement.setAttribute("height", "24");
    svgElement.setAttribute("viewBox", "0 0 24 24");
    svgElement.setAttribute("fill", "none");
    svgElement.style.cursor = 'pointer';
    svgElement.classList.add("icon-sm");

    const pathElement = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathElement.setAttribute("fill-rule", "evenodd");
    pathElement.setAttribute("clip-rule", "evenodd");
    pathElement.setAttribute("d", "M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z");
    pathElement.setAttribute("fill", "currentColor");

    svgElement.appendChild(pathElement);

    const closeButton = document.createElement('button');
    closeButton.textContent = 'X';
    closeButton.style.background = 'none';
    closeButton.style.border = 'none';
    closeButton.style.color = 'white';
    closeButton.style.cursor = 'pointer';
    closeButton.style.fontSize = '16px';

    closeButton.addEventListener('click', function() {
        document.body.removeChild(movableWindow);
    });

    svgElement.addEventListener('click', function(){
        navigator.clipboard.writeText(document.getElementById(textArea.id).textContent);
        console.log("here");
        console.log(document.getElementById(textArea.id).textContent);
    });

    let isDragging = false;
    let offsetX, offsetY;

    const onMouseDown = (e) => {
        const rect = movableWindow.getBoundingClientRect();
        const borderWidth = 10;

        if (e.clientY < rect.top + borderWidth) 
        {
            isDragging = true;
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        }
    };

    const onMouseMove = (e) => {
        if (isDragging) {
            movableWindow.style.left = `${e.clientX - offsetX}px`;
            movableWindow.style.top = `${e.clientY - offsetY}px`;
        }
    };

    const onMouseUp = () => {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    };

    movableWindow.addEventListener('mousedown', onMouseDown);

    const controlContainer = document.createElement('div');
    controlContainer.style.position = 'absolute';
    controlContainer.style.top = '5px';
    controlContainer.style.right = '5px';
    controlContainer.style.display = 'flex';
    controlContainer.style.alignItems = 'center';
    controlContainer.style.gap = '20px';
   
    controlContainer.appendChild(svgElement);
    controlContainer.appendChild(closeButton);

    movableWindow.appendChild(textArea);
    movableWindow.appendChild(controlContainer);
    document.body.appendChild(movableWindow);

    function typeText(text, delay = 100) {
        const textArea = document.getElementById("text-text-area-1234");
        if (!textArea) return;
    
        let index = 0;
    
        const interval = setInterval(() => {
            if (index < text.length) {
                textArea.textContent += text[index];
                index++;
            } else {
                clearInterval(interval);
            }
        }, delay);
    }

    function getHighlightedText() {
        const selectedText = window.getSelection().toString();
        return selectedText;
    }
    
    typeText(getHighlightedText())    
})();
