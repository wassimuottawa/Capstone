import {Component, EventEmitter, Host, OnInit, Output, QueryList, ViewChildren, ViewEncapsulation} from '@angular/core';
import {FolderComponent} from "../folder/folder.component";
import {HomeComponent} from "../home/home.component";

@Component({
  selector: 'app-action-menu',
  templateUrl: './action-menu.component.html',
  styleUrls: ['./action-menu.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ActionMenuComponent implements OnInit {

  @Output() onDeselectAll: EventEmitter<void> = new EventEmitter<void>()
  @Output() onDelete: EventEmitter<void> = new EventEmitter<void>()

  constructor() { }

  ngOnInit(): void {
  }

  deselectAll() {
    this.onDeselectAll.emit()
  }

  delete() {
    this.onDelete.emit();
  }
}
