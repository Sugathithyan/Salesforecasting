import { HttpClient, HttpResponseBase } from '@angular/common/http';
import { ReadPropExpr } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route,Router } from '@angular/router';
import { LoginComponent } from '../login/login.component';
import { ProserviceService } from '../proservice.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {
  signup:any= FormGroup;
  url1 = "http://localhost:5000/api/register_user";

  constructor(private http: HttpClient,private fb:FormBuilder,private route: Router,private ps:ProserviceService,private snb:MatSnackBar) { }
  
  ngOnInit(): void {
    this.signup=this.fb.group(
      {
        email:['',Validators.compose([Validators.required,Validators.email])],
        pass:['',Validators.compose([Validators.required,Validators.minLength(5)])],
        repass:['',Validators.compose([Validators.required,Validators.minLength(5)])]
      }
    )
  }
 
  onsubmit(data: any)
  {

   let params={
    email:data.email,
    pass:data.pass,
   }
   if(data.pass==data.repass)
   {
    this.http.post(this.url1,params).subscribe((data:any)=>{});
    this.snb.open(' Registered Successfully........Proceed Login ', 'close', {duration: 3000});
    this.route.navigate(['login'])
   }
   else{
    this.snb.open('Password Mismatch','close',{duration: 2000});
   }
  }
  goToLogin()
  {
-
   this.route.navigate(['login']);
  }
}
