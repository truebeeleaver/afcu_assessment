function doLogout() {
  _resetErrors();

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 201) {
        document.location = "login";
      } else {
        _displayError("An unexpected error has occurred.");
        console.error(this);
      }
    }
  };
  xhr.open("POST", "api/profile/logout", true);
  xhr.send();
}

function fetchProfile() {
  _resetErrors();
  _setLoading(true);

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        resp = JSON.parse(this.responseText);
        _displayProfile(resp["email"], resp["phone"]);
        _setLoading(false);
      } else if (this.status == 401) {
        document.location="login";
      } else {
        _displayError("An unexpected error has occurred.");
        console.error(this);
      }
    }
  };
  xhr.open("GET", "api/profile", true);
  xhr.send();
}

function _setLoading(isLoading) {
  var loading = document.getElementById("loading");
  loading.hidden = !isLoading;
  profile.hidden = isLoading;
}

function _displayProfile(email, phone) {
  var elem_email = document.getElementById("email")
  var elem_phone = document.getElementById("phone");
  elem_email.innerHTML = email;
  elem_phone.innerHTML = phone;
  elem_email.hidden = false;
  elem_phone.hidden = false;
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
