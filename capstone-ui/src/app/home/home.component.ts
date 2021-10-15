import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ThemePalette} from "@angular/material/core";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  panelOpenState = false;

  folders = ['Folder 1', 'Folder 2', 'Folder 3', 'Folder 4', 'Folder 5']

  links = ['Home'];
  activeLink = 0;
  background: ThemePalette = undefined;

  toggleBackground() {
    this.background = this.background ? undefined : 'primary';
  }

  addLink() {
    this.links.push(`Tab ${this.links.length + 1}`);
    this.activeLink = this.links.length-1
  }

  isHomeTab(tab : String) {
    return tab == 'Home'
  }

}
