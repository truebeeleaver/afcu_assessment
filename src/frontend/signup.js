function doSignup() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password_box").value;
  var password_confirm = document.getElementById("password_confirm").value;
  var phone = document.getElementById("phone").value;
  _doSignup(email, password, password_confirm, phone);
}

function _resetErrors() {
  var errorbanner = document.getElementById("error");
  errorbanner.hidden = true;

  var email_error = document.getElementById("error_email");
  email_error.hidden = true;
  var password_error = document.getElementById("error_password");
  password_error.hidden = true;
  var phone_error = document.getElementById("error_phone");
  phone_error.hidden = true;
}

function _displayError(field, message) {
  if (!field) {
    var errorbanner = document.getElementById("error");
    errorbanner.hidden = false;
    errorbanner.innerHTML = message;
  } else {
    fielderror = document.getElementById("error_" + field);
    if (fielderror) {
      fielderror.hidden = false;
      fielderror.innerHTML = message;
    } else {
      console.error(message);
    }
  }
}

function _doSignup(email, password, password_confirm, phone) {
  _resetErrors();

  if (password != password_confirm) {
    _displayError("password", "Password does not match.");
    return;
  }

  content = {"email": email, "password": password, "phone": phone};

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 201) {
        document.location = "profile";
      } else {
        resp = JSON.parse(this.responseText);
        if (resp.hasOwnProperty("field_errors")) {
          var errors = resp["field_errors"];
          for (var prop in errors) {
            // Unashamed that I stackoverflow'd this; JS is crazy
            if (Object.prototype.hasOwnProperty.call(errors, prop)) {
              _displayError(prop, errors[prop]);
            }
          }
        } else {
          _displayError(null, "An unexpected error has occurred.");
          console.error(this);
        }
      }
    }
  };
  xhr.open("POST", "api/profile/signup", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(content));
}
