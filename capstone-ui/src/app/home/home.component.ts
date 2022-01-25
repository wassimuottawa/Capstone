import {Component, QueryList, ViewChildren, ViewEncapsulation, HostListener} from '@angular/core';
import {MatSnackBar} from "@angular/material/snack-bar";
import {ActionMenuComponent} from "../action-menu/action-menu.component";
import {FolderComponent} from "../folder/folder.component";
import {BackendService} from "../service/backend.service";
import {FormControl} from "@angular/forms";

export enum KEY_CODE {
  EXTRACT = 88,     //X
  DELETE = 46,    //DELETE
  DESELECT = 27,  //ESC
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent {

  @ViewChildren('folderComponent') folders: QueryList<FolderComponent> = new QueryList<FolderComponent>()

  invisibleFolders: Set<string> = new Set()
  folderToSelectedImagesMap: Map<string, Set<string>> = new Map();
  scrollThreshold: number = 0.8 //to load more items if user beyond (x*100)% of the screen
  lastLoadDate: Date = new Date()
  waitBetweenLoadMore = 500 //0.5s
  visibleFolders: Set<string> = new Set()
  actionMenuOpen: boolean = false
  runs: string[] = []
  run = ""
  defaultStartTime = '00:00'
  defaultEndTime = '23:59'
  appliedStartTime : string = this.defaultStartTime //keep track of the last filter when user clicks "apply", reset to this value if form is modified without clicking apply
  appliedEndTime: string = this.defaultEndTime
  startTimeForm: FormControl = new FormControl(this.defaultStartTime)
  endTimeForm: FormControl = new FormControl(this.defaultEndTime)
  foldersPerScreen: number = 5

  @HostListener('window:keyup', ['$event'])
    keyEvent(event: KeyboardEvent) {
      console.log(event);

      if (event.keyCode === KEY_CODE.EXTRACT) {
        this.click();
      }
      if (event.keyCode === KEY_CODE.DELETE) {
        this.click();
      }
      if (event.keyCode === KEY_CODE.DESELECT) {
        this.click();
      }
    }

  constructor(private snackBar: MatSnackBar, private service: BackendService) {
    service.getRuns().subscribe(runs => {
      this.runs = runs
      this.run = runs[0] ?? ""
      this.loadFolders()
    })
  }

  refreshContent() {
    this.clearSelection()
    this.invisibleFolders.clear()
    this.visibleFolders.clear()
    this.lastLoadDate = new Date()
    this.closeActionMenu()
    this.loadFolders()
  }

  loadFolders() {
    this.service.getFolders(this.run).subscribe((foldersToFileNames: any) => {
      foldersToFileNames.forEach((folder: any) => {
        this.invisibleFolders.add(folder)
      })
      this.addFoldersToViewport(this.foldersPerScreen)
    })
  }

  getFolders(): string[] {
    return [...this.visibleFolders]
  }

  openActionMenu() {
    if (!this.actionMenuOpen) {
      let matRef = this.snackBar.openFromComponent(ActionMenuComponent, {}).instance
      this.actionMenuOpen = true
      matRef.onDeselectAll.subscribe(() => {
        this.deselectAll()
        this.closeActionMenu()
      });
      matRef.onDelete.subscribe(() => {
        this.deleteSelected();
        this.closeActionMenu();
      })
    }
  }

  closeActionMenu() {
    this.snackBar.dismiss()
    this.actionMenuOpen = false
  }

  removeEmptyFolder(folder: string) {
    this.visibleFolders.delete(folder)
    this.addFoldersToViewport(1)
  }

  applyTimeFilter() {
    this.appliedStartTime = this.startTimeForm.value
    this.appliedEndTime = this.endTimeForm.value
    this.refreshContent()
  }

  resetTimeFiler() {
    this.appliedStartTime = this.defaultStartTime
    this.appliedEndTime = this.defaultEndTime
    this.refreshContent()
  }

  filterMenuOpened() {
    this.startTimeForm.setValue(this.appliedStartTime)
    this.endTimeForm.setValue(this.appliedEndTime)
  }

  addFoldersToViewport(count: number = 2) {
    let curr = 0
    let newFolders = []
    for (let folder of this.invisibleFolders) {
      if (curr >= count) break
      newFolders.push(folder)
      curr++
    }
    newFolders.forEach(folder => {
      this.invisibleFolders.delete(folder)
      this.visibleFolders.add(folder)
    })
  }

  deleteSelected() {
    this.service.delete(this.run, this.folderToSelectedImagesMap).subscribe(() => {
        this.folders.filter(folder => this.folderToSelectedImagesMap.has(folder.folder)).forEach(folder => folder.deleteSelected())
        this.clearSelection()
      }
    )
  }

  onScroll(event: any) {
    if (this.invisibleFolders.size) {
      const scrolledBeyondThreshold = event.target.offsetHeight + event.target.scrollTop >= this.scrollThreshold * event.target.scrollHeight
      if (scrolledBeyondThreshold) {
        let timeElapsedAfterLastLoad = new Date().getTime() - this.lastLoadDate.getTime()
        if (timeElapsedAfterLastLoad > this.waitBetweenLoadMore) {
          this.addFoldersToViewport()
        }
      }
    }
  }

  deselectAll() {
    this.folders.forEach(folder => folder.deselectAll())
    this.clearSelection()
  }

  clearSelection() {
    this.folderToSelectedImagesMap.clear()
  }

  onSelectionChange(selectedImages: Set<string>, folder: string) {
    selectedImages.size ? this.folderToSelectedImagesMap.set(folder, selectedImages) : this.folderToSelectedImagesMap.delete(folder)
    this.folderToSelectedImagesMap.size ? this.openActionMenu() : this.closeActionMenu()
  }

  click(){
    console.log("Hit")
  }
}
