import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Validators } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';
import { FormGroup,FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { NgbAlert, NgbAlertModule } from '@ng-bootstrap/ng-bootstrap';
import { ProserviceService } from '../proservice.service';
import { SignupComponent } from '../signup/signup.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  
  login:any=FormGroup;
  users:any=[];
  url = "http://localhost:5000/api/read-users";

  constructor(private fb:FormBuilder,private route: Router,private proser: ProserviceService,private http: HttpClient,private snb: MatSnackBar){}
  ngOnInit(): void {
    this.login=this.fb.group({
        email:['',Validators.compose([Validators.required,Validators.email])],
        pass:['',Validators.compose([Validators.required,Validators.minLength(5)])]
      })

    this.http.get<any>(this.url).subscribe((data: any) => {
        this.users = data['data'];
        console.log(this.users);
      });
    
  }
  onlogin(data:any)
  {
    if(data.email)
    {
        this.users.forEach((item:any) => {
        if(item.email == data.email && item.pass == data.pass){
          console.log(data)
          this.snb.open('Logged Successfully', 'close', {duration: 3000});
          this.route.navigate(['file-upload'])
        }
        else{
          localStorage.clear();
         }
        });
    }
  }
  goToSignup()
  {
    this.route.navigate(['signup']);
  }
}
