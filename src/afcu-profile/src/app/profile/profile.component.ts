import { Component, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { ErrorbannerComponent } from '../errorbanner/errorbanner.component'; 

interface Profile {
  username: string;
  phone: string;
}

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.less']
})
export class ProfileComponent implements OnInit {

  profile: Profile = null
  errormessage: string = ""

  constructor(private http: HttpClient, private router: Router) { }

  doLogout(): void {
    this.http.post('api/profile/logout', null)
    .subscribe(
      data => this.router.navigate(['login']),
      error => this.handleError(error) 
    );
  }

  handleError(error): void {
    if (error.status == 401) {
      this.router.navigate(['login']);
    }
    else
    {
      console.error(error);
      this.errormessage = "An unexpected error has occurred.";
    }
  }

  ngOnInit(): void {
    this.http.get<Profile>('api/profile')
    .subscribe(
      (data: Profile) => this.profile = { ...data },
      error => this.handleError(error) 
    );
  }


}
