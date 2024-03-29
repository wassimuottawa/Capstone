import {AfterViewInit, Component, HostListener, QueryList, ViewChildren, ViewEncapsulation} from '@angular/core';
import {FolderComponent} from "../folder/folder.component";
import {BackendService} from "../service/backend.service";
import {FormControl} from "@angular/forms";
import {Utils} from "../utils/utils";

export enum KEYBOARD_SHORTCUTS {
  MERGE = 'x',
  DELETE = 'delete',
  DESELECT = 'escape'
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent implements AfterViewInit {

  @ViewChildren('folderComponent') folders: QueryList<FolderComponent> = new QueryList<FolderComponent>()

  hiddenFolders: Map<string, string[]> = new Map()
  folderToSelectedTrackletsMap: Map<string, Set<string>> = new Map();
  scrollThreshold: number = 0.8 //to load more items if user beyond (x*100)% of the screen
  lastLoadDate: Date = new Date()
  waitBetweenLoadMore = 500 //0.5s
  visibleFolders: Map<string, string[]> = new Map()
  runs: string[] = []
  run = ""
  defaultStartTime = '00:00'
  defaultEndTime = '23:59'
  //keep track of the last filter when user clicks "apply", reset to this value if form is modified without clicking apply
  appliedStartTime: string = this.defaultStartTime
  appliedEndTime: string = this.defaultEndTime
  startTimeForm: FormControl = new FormControl(this.defaultStartTime)
  endTimeForm: FormControl = new FormControl(this.defaultEndTime)
  trackletsPerScreen: number = 5
  shortcuts = KEYBOARD_SHORTCUTS
  imageHeight = 198
  mainContainer: HTMLElement | undefined
  operationRunning = false
  endOfItems = false
  mode = 'annotate'

  @HostListener('window:keyup', ['$event'])
  keyEvent(event: KeyboardEvent) {
    const key = event.key?.toLowerCase()
    if (key === KEYBOARD_SHORTCUTS.MERGE) this.mergeSelectedTracklets()
    else if (key === KEYBOARD_SHORTCUTS.DELETE) this.deleteSelected()
    else if (key === KEYBOARD_SHORTCUTS.DESELECT) this.deselectAll()
  }

  constructor(private service: BackendService) {
  }

  ngAfterViewInit() {
    this.mainContainer = document.getElementById('main-container')!
    this.trackletsPerScreen = Math.ceil(this.mainContainer.offsetHeight / this.imageHeight)
    this.service.getRuns().subscribe(runs => {
      this.runs = runs
      this.run = runs[0] ?? ""
      this.loadFolders()
    })
  }

  refreshContent() {
    this.clearSelection()
    this.hiddenFolders.clear()
    this.visibleFolders.clear()
    this.lastLoadDate = new Date()
    this.endOfItems = false
    this.loadFolders()
  }

  loadFolders() {
    this.service.getFoldersToTrackletsMap(this.run, this.appliedStartTime, this.appliedEndTime)
      .subscribe((foldersToTracklets) => {
        Object.entries(foldersToTracklets).forEach(([folder, tracklets]) => {
          this.hiddenFolders.set(folder, tracklets)
        })
        this.addFoldersToViewport(this.trackletsPerScreen)
      })
  }

  isAnnotate() {
    return this.mode == 'annotate'
  }

  isStatistics() {
    return this.mode == 'statistics'
  }

  getFolders(): string[] {
    return Utils.getKeysFromMap(this.visibleFolders)
  }

  getTrackletsByFolder(folder: string): string[] {
    return this.visibleFolders.get(folder) ?? []
  }

  removeEmptyFolder(folder: string) {
    this.visibleFolders.delete(folder)
    this.addFoldersUntilScreenFilled()
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

  mergeSelectedTracklets() {
    if (!this.isSelectionEmpty()) {
      this.operationRunning = true
      this.service.mergeIntoNewFolder(this.run, this.folderToSelectedTrackletsMap).subscribe(destinationFolder => {
        this.visibleFolders.has(destinationFolder) ?
          this.folders.filter(f => f.folder === destinationFolder)[0].loadImageNames() :
          this.hiddenFolders.set(
            destinationFolder,
            Array.from(this.folderToSelectedTrackletsMap.values())
              .map(set => [...set])
              .reduce((accumulator, value) => accumulator.concat(value), [])
          )
        this.removeSelectedTrackletsFromUI(destinationFolder)
        this.operationRunning = false
      })
    }
  }

  addFoldersUntilScreenFilled() {
    setTimeout(() => {
      (this.mainContainer?.scrollHeight! - 100 <= this.mainContainer?.offsetHeight!) ?
        this.addFoldersToViewport(1) :
        this.checkIfEndOfItems()
    }, 500)
  }

  addFoldersToViewport(count: number = 2) {
    let curr = 0
    let newFolders = new Map<string, string[]>()
    for (let [folder, tracklets] of this.hiddenFolders) {
      if (curr >= count) break
      newFolders.set(folder, tracklets)
      curr += tracklets.length
    }
    newFolders.forEach((tracklets, folder) => {
      this.hiddenFolders.delete(folder)
      this.visibleFolders.set(folder, tracklets)
    })
    this.checkIfEndOfItems()
  }

  checkIfEndOfItems() {
    if (!this.hiddenFolders.size) this.endOfItems = true
  }

  deleteSelected() {
    if (!this.isSelectionEmpty()) {
      this.operationRunning = true
      this.service.delete(this.run, this.folderToSelectedTrackletsMap).subscribe(() => {
        this.removeSelectedTrackletsFromUI()
        this.operationRunning = false
      })
    }
  }

  getShortcutString(shortcut: KEYBOARD_SHORTCUTS) {
    return shortcut.toString().substr(0, 3).toUpperCase()
  }

  removeSelectedTrackletsFromUI(existingFolder?: string) {
    this.folders.filter(folder => folder.folder != existingFolder && this.folderToSelectedTrackletsMap.has(folder.folder))
      .forEach(folder => folder.deleteSelectedTracklets())
    this.clearSelection()
    this.addFoldersUntilScreenFilled()
  }

  onScroll(event: any) {
    if (this.hiddenFolders.size) {
      const containerEl = event.target
      if (containerEl.offsetHeight + containerEl.scrollTop >= this.scrollThreshold * containerEl.scrollHeight) {
        let timeElapsedAfterLastLoad = new Date().getTime() - this.lastLoadDate.getTime()
        if (timeElapsedAfterLastLoad > this.waitBetweenLoadMore) {
          this.addFoldersToViewport()
        }
      }
    }
  }

  deselectAll() {
    this.folders.forEach(folder => folder.deselectAllTracklets())
    this.clearSelection()
  }

  isSelectionEmpty(): boolean {
    return !Boolean(this.folderToSelectedTrackletsMap.size)
  }

  clearSelection() {
    this.folderToSelectedTrackletsMap.clear()
  }

  onSelectionChange(selectedTracklets: Set<string>, folder: string) {
    selectedTracklets.size ? this.folderToSelectedTrackletsMap.set(folder, selectedTracklets) : this.folderToSelectedTrackletsMap.delete(folder)
  }

  isActionButtonsDisabled() {
    return this.operationRunning || this.isSelectionEmpty()
  }
}
