import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';
import { Router } from '@angular/router';

@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.css']
})
export class DisplayComponent implements OnInit {
 
  templist:any=[];
  passengers:any=[];
  forevalue:any=[];
  dates: any =[];
  ms:any=[];
  schar=false
  smet=false


  constructor(private http:HttpClient,private route:Router) { Chart.register(... registerables)}
 
  ngOnInit(): void {
    let nurl = "http://localhost:5000/api/get_data"
    this.http.get<any>(nurl).subscribe((data) => {
      
      this.templist = data;
      this.ms=this.templist['metrics']
      console.log(this.ms)
      for (let i = 0; i < this.templist['passengers'].length; i++) {
        let t1 = this.templist['date'][i]
        let t2 = Number(this.templist['passengers'][i])
        let cord = {
          x: t1, y: t2
        }
        this.dates.push(t1);
        this.passengers.push(cord);
      }

      for (let i = 0; i < this.templist['forecast'].length; i++) {
        let t1 = this.templist['date'][this.templist['passengers'].length + i]
        let t2 = Number(this.templist['forecast'][i])
        let cord = {
          x: t1, y: t2
        }
        this.dates.push(t1);
        this.forevalue.push(cord);
      }
      console.log(this.dates);
      console.log(this.passengers);
      console.log(this.forevalue);
    });

  }
  getdata() {
    this.schar=true
    this.smet=false
    const hello = new Chart('myChart', {
			type: 'line',
			data: {
				labels: this.dates,
				datasets: [{
					label: 'Trained',
					data: this.passengers,
					tension: 0.3,
					borderColor:'rgba(100,25,12)',
					backgroundColor: 'rgba(120, 20, 320)'
				},
				{
					label: 'Forecast',
					data: this.forevalue,
					tension: 0.3,
					borderColor: 'rgba(242, 120, 63)',
					backgroundColor: 'rgba(242, 120, 63)'
			}]
			},
			options: {
				scales: {

				}
			}
		});
  }
  formetrics()
  {
    this.smet=true
    this.schar=false
  }
  onback()
  {
    this.route.navigate(['file-upload'])
  }
  routelogout()
  {
    this.route.navigate(['signup'])
  }
}
