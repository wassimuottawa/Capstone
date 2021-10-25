import {Component, ViewEncapsulation} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent {

  invisibleFolders: Set<string> = new Set()
  folderToSelectedImagesMap: Map<string, Set<string>> = new Map();
  endOfItems: boolean = false
  scrollThreshold: number = 0.9 //to load more items if user beyond (x*100)% of the screen
  lastLoadDate: Date = new Date()
  waitBetweenLoadMore = 500 //0.5s
  visibleFolders: Set<string> = new Set()

  constructor(private http: HttpClient) {
    http.get("http://127.0.0.1:5000/folders").subscribe((foldersToFileNames: any) => {
      foldersToFileNames.forEach((folder: any) => {
        this.invisibleFolders.add(folder)
      })
      this.loadMore(5)
    })
  }

  getFolders(): string[] {
    return [...this.visibleFolders]
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

  onSelectionChange(selectedImages: Set<string>, folder: string) {
    selectedImages.size ? this.folderToSelectedImagesMap.set(folder, selectedImages) : this.folderToSelectedImagesMap.delete(folder)
  }
}
