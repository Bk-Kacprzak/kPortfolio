const mainContainer = document.querySelector(".content-container");

const showForm = (formToOpenClass, anotherFormClass = null) => { 
    if (anotherFormClass != null) { 
        anotherForm = document.querySelector(anotherFormClass);
        if (anotherForm.style.display == "block") 
            return;
    }
  
    form = document.querySelector(formToOpenClass) 
    mainContainer.setAttribute("style", "opacity: 0.2");
    form.setAttribute("style", "display: block");
}

const hideForm = (formClasses) => { 
    formClasses.forEach((value)=> { 
        form = document.querySelector(value) 
        form.setAttribute("style", "display: none");
    })
    mainContainer.setAttribute("style", "opacity: 1");
}

const blockTypeNonNumericInput = (event) => { 
    // TODO: fix bug - paste shortcut works and enable to paste non-numeric input
    if (event.key.length === 1 && /\D/.test(event.key)) {
        event.preventDefault();
      }

    if ( this !== event.target && 
    ( /textarea|select/i.test( event.target.nodeName ) ||
        event.target.type === "text") ) {
            return;
    }
}   