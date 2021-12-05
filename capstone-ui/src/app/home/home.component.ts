import {Component, QueryList, ViewChildren, ViewEncapsulation} from '@angular/core';
import {MatSnackBar} from "@angular/material/snack-bar";
import {ActionMenuComponent} from "../action-menu/action-menu.component";
import {FolderComponent} from "../folder/folder.component";
import {HttpService} from "../service/HttpService";

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
  endOfItems: boolean = false
  scrollThreshold: number = 0.8 //to load more items if user beyond (x*100)% of the screen
  lastLoadDate: Date = new Date()
  waitBetweenLoadMore = 500 //0.5s
  visibleFolders: Set<string> = new Set()
  actionMenuOpen: boolean = false
  runs: string[] = []
  run = ""

  constructor(private _snackBar: MatSnackBar, private service: HttpService) {
    service.getRuns().subscribe(runs => {
      this.runs = runs
      this.run = runs[0] ?? ""
      this.loadFolders()
    })
  }

  runChanged() {
    this.invisibleFolders.clear()
    this.folderToSelectedImagesMap.clear()
    this.endOfItems = false
    this.lastLoadDate = new Date()
    this.visibleFolders.clear()
    this.closeActionMenu()
    this.loadFolders()
  }

  loadFolders() {
    this.service.getFolders(this.run).subscribe((foldersToFileNames: any) => {
      foldersToFileNames.forEach((folder: any) => {
        this.invisibleFolders.add(folder)
      })
      this.loadMore(5)
    })
  }

  getFolders(): string[] {
    return [...this.visibleFolders]
  }

  openActionMenu() {
    if (!this.actionMenuOpen) {
      let matRef = this._snackBar.openFromComponent(ActionMenuComponent, {}).instance
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
    this._snackBar.dismiss()
    this.actionMenuOpen = false
  }

  loadMore(count: number = 2) {
    let curr = 0
    let newFolders = []
    for (let fld of this.invisibleFolders) {
      if (curr >= count) break
      newFolders.push(fld)
      curr++
    }
    newFolders.forEach(folder => {
      this.invisibleFolders.delete(folder)
      this.visibleFolders.add(folder)
    })
    if (this.invisibleFolders.size == 0) {
      this.endOfItems = true
    }
  }

  deleteSelected() {
    this.service.delete(this.run, this.folderToSelectedImagesMap).subscribe(() =>
      this.folders.filter(folder => this.folderToSelectedImagesMap.has(folder.folder)).forEach(
        folder => folder.deleteSelected()
      )
    )
  }

  onScroll(event: any) {
    if (!this.endOfItems) {
      const scrolledBeyondThreshold = event.target.offsetHeight + event.target.scrollTop >= this.scrollThreshold * event.target.scrollHeight
      if (scrolledBeyondThreshold) {
        let timeFromLastLoad = new Date().getTime() - this.lastLoadDate.getTime()
        if (timeFromLastLoad > this.waitBetweenLoadMore) {
          this.loadMore()
        }
      }
    }
  }

  deselectAll() {
    this.folders.forEach(folder => {
      folder.deselectAll()
    })
    this.folderToSelectedImagesMap.clear()
  }

  onSelectionChange(selectedImages: Set<string>, folder: string) {
    if (selectedImages.size) {
      this.folderToSelectedImagesMap.set(folder, selectedImages)
      this.openActionMenu()
    } else {
      this.folderToSelectedImagesMap.delete(folder)
      this.closeActionMenu()
    }
  }
}
