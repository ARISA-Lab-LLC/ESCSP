function showView(show, view) {
  const display = show ? "flex" : "none";
  var viewElement = document.getElementById(view);
  viewElement.style.display = display;
}

function onRegister(event) {
  event.preventDefault();
  document.getElementById("audioMothForm").submit();
}

function validateForm() {
  var emailElement = document.getElementById("email");
  var zipElement = document.getElementById("zip");
  var serialElement = document.getElementById("serial");

  var elements = [emailElement, zipElement, serialElement];

  var validForm = true;

  for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    if (!element.checkValidity()) {
      element.reportValidity();
      validForm = false;
      break;
    }
  }

  return validForm;
}

function register() {
  showView(true, "spinner");
  document.getElementById("registerButton").disabled = true; 

  const email = document.getElementById("email").value.trim();
  const zip = document.getElementById("zip").value.trim();
  const serial = document.getElementById("serial").value.trim();

  registerAudioMothUser(email, zip, serial, function (response) {
    showView(false, "spinner");
    document.getElementById("registerButton").disabled = false; 

    if (response == null) {
      alert("Failed to register, please try again.");
      return;
    }

    if (response["success"]) {
      showRegistrationComplete(response["data"]);
    } else {
      const errors = response["errors"];
      var error_message = "Failed to register due to the following field errors:\n"
      
      Object.entries(errors).forEach(([key, value]) => {
        if (value.length > 0) {
          error_message += `- \n${key}: ${value}`;
        }
      });

      error_message += "\n\nPlease fix the errors above and try again."
      alert(error_message);
    }
  });
}

function showRegistrationComplete(data) {
  showView(false, "formView");
  showView(true, "resultView");

  jQuery("#idTerm").text("AudioMoth ID");
  jQuery("#emailTerm").text("Email");
  jQuery("#zipTerm").text("Zip Code");
  jQuery("#serialTerm").text("AudioMoth Serial Number");

  jQuery("#idDetail").text(data["id"]);
  jQuery("#emailDetail").text(data["email"]);
  jQuery("#zipDetail").text(data["zip_code"]);
  jQuery("#serialDetail").text(data["serial_number"]);
}

jQuery(document).ready(function ($) {

  document.getElementById("audioMothForm").reset();

  jQuery("#registerButton").on("click", function (event) {
    event.preventDefault();
    jQuery("#audioMothForm").trigger("submit");
  });

  jQuery("#audioMothForm").on("submit", function (event) {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    register();
  });

  showView(false, "spinner");
  showView(false, "resultView");
  showView(true, "formView");
});

