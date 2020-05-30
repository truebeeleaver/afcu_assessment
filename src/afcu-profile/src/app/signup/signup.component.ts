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

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
  }
  
  doSignup(): void {
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

  handleError(error): void {
    console.error(error);
    this.errormessage = "An unexpected error has occurred.";
  }

}
