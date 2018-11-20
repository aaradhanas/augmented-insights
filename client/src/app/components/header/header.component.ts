import { Component, OnInit, ViewEncapsulation} from '@angular/core';
import { DataService } from "../../services/data.service";
import { Router } from '@angular/router';

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.css'],
    encapsulation: ViewEncapsulation.None
})
export class HeaderComponent implements OnInit{
    constructor(private dataService: DataService, private router: Router){
        
    }
    
    ngOnInit(){

    }

    navigateToHomePage(){
        this.router.navigate(['home']);
    }

    invokeClickEvent(){
        this.dataService.onGenerateInsight();
    }
}