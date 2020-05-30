import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

const httpOptions = {
  headers: new HttpHeaders({
    "Content-Type": "application/json"
  })
}

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.less']
})
export class SignupComponent implements OnInit {
  username: string = ""
  password: string = ""
  confirm_password: string = ""
  phone: string = ""
  errormessage: string = ""
  field_errors: object = {} 

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
  }

  checkPasswordMatch(): boolean {
    if (this.password != this.confirm_password) {
      this.field_errors['password'] = "Password does not match";  
      return false;
    }
    return true;
  }
  
  doSignup(): void {
    if (!this.checkPasswordMatch()) {
      return;
    }
    var profile = { "username" : this.username, "password" : this.password, "phone" : this.phone };
    this.http.post('api/profile/signup', profile, httpOptions)
    .subscribe(
      data => this.handleSignup(data),
      error => this.handleError(error) 
    );
  }

  handleSignup(data): void {
      this.router.navigate(['']);
  }

  handleError(resp): void {
    if (resp.error.field_errors) {
      this.errormessage = "Sign up failed.";
      this.field_errors = { ...resp.error.field_errors };
    } else {
      console.error(resp);
      this.errormessage = "An unexpected error has occurred.";
    }
  }

}
