import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

const httpOptions = {
  headers: new HttpHeaders({
    "Content-Type": "application/json"
  })
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent {
  email: string = ""
  password: string = ""
  errormessage: string = ""

  constructor(private http: HttpClient, private router: Router) { }

  doLogin(): void {
    var auth = { "email" : this.email, "password" : this.password };
    this.http.post('api/profile/login', auth, httpOptions)
    .subscribe(
      data => this.handleLogin(data),
      error => this.handleError(error) 
    );
  }

  handleLogin(data): void {
      this.router.navigate(['']);
  }

  handleError(resp): void {
    if (resp.status == 401) {
      this.errormessage = "Login attempt unsuccessful.";
    } else {
      console.error(resp);
      this.errormessage = "An unexpected error has occurred.";
    }
  }

}
