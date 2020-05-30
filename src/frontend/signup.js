function doSignup() {
  errorbanner = document.getElementById("error");
  errorbanner.hidden = true;
  email = document.getElementById("email").value;
  password = document.getElementById("password_box").value;
  password_confirm = document.getElementById("password_confirm").value;
  phone = document.getElementById("phone").value;

  if (password != password_confirm) {
    errorbanner.hidden = false;
    errorbanner.innerHTML = "Password does not match.";
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
          errorbanner.hidden = true;
          var errors = resp['field_errors'];
          for (var prop in errors) {
            // Unashamed that I stackoverflow'd this; JS is crazy
            if (Object.prototype.hasOwnProperty.call(errors, prop)) {
              var id = "error_" + prop;
              var field_error = document.getElementById(id);
              if (field_error) {
                field_error.hidden = false;
                field_error.innerHTML = errors[prop];
              }
            }
          }
        } else {
          errorbanner.hidden = false;
          errorbanner.innerHTML = "An unexpected error has occurred.";
          console.error(this);
        }
      }
    }
  };
  xhr.open("POST", "api/profile/signup", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(content));
}
