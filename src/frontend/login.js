function doLogin() {
  errorbanner = document.getElementById("error");
  errorbanner.hidden = true;
  email = document.getElementById("email").value;
  password = document.getElementById("password").value;
  content = {"email": email, "password": password};

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState == 4) {
      if (this.status == 201) {
        document.location = "profile";
      } else if (this.status == 401) {
        errorbanner.hidden = false;
        errorbanner.innerHTML = "Login attempt unsuccessful.";
      } else {
        errorbanner.hidden = false;
        errorbanner.innerHTML = "An unexpected error has occurred.";
        console.error(this);
      }
    }
  };
  xhr.open("POST", "api/profile/login", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(content));
}
