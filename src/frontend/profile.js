function doLogout() {
  errorbanner = document.getElementById("error");
  errorbanner.hidden = true;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 201) {
        document.location = "login";
      } else {
        errorbanner.hidden = false;
        errorbanner.innerHTML = "An unexpected error has occurred.";
        console.error(this);
      }
    }
  };
  xhr.open("POST", "api/profile/logout", true);
  xhr.send();
}

function fetchProfile() {
  errorbanner = document.getElementById("error");
  errorbanner.hidden = true;

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 200) {
        resp = JSON.parse(this.responseText);
        console.log(resp);
        document.getElementById("email").innerHTML = resp['email'];
        document.getElementById("phone").innerHTML = resp['phone'];
        document.getElementById("profile").hidden = false;
        document.getElementById("loading").hidden = true;
      } else if (this.status == 401) {
        document.location="login";
      } else {
        errorbanner.hidden = false;
        errorbanner.innerHTML = "An unexpected error has occurred.";
        console.error(this);
      }
    }
  };
  xhr.open("GET", "api/profile", true);
  xhr.send();
}
