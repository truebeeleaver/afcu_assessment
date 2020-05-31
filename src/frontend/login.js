function doLogin() {
  email = document.getElementById("email").value;
  password = document.getElementById("password").value;
  _doLogin(email, password);
}

function _resetErrors() {
  var errorbanner = document.getElementById("error");
  errorbanner.hidden = true;
}

function _displayError(message) {
  var errorbanner = document.getElementById("error");
  errorbanner.hidden = false;
  errorbanner.innerHTML = message;
}

function _doLogin(email, password) {
  _resetErrors();
  
  content = {"email": email, "password": password};

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 201) {
        document.location = "profile";
      } else if (this.status == 401) {
        _displayError("Login attempt unsuccessful.");
      } else {
        _displayError("An unexpected error has occurred.");
        console.error(this);
      }
    }
  };
  xhr.open("POST", "api/profile/login", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(content));
}
