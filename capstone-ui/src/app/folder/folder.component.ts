import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  QueryList,
  ViewChild,
  ViewChildren,
  ViewEncapsulation
} from '@angular/core';
import {BackendService} from "../service/backend.service";
import {TrackletComponent} from "../tracklet/tracklet.component";
import {Utils} from "../utils/utils";

@Component({
  selector: 'app-folder',
  templateUrl: './folder.component.html',
  styleUrls: ['./folder.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FolderComponent implements AfterViewInit {
  @Output() onSelectionChange: EventEmitter<Set<string>> = new EventEmitter<Set<string>>()
  @Output() isEmpty: EventEmitter<void> = new EventEmitter<void>()
  @Output() folderCollapsed: EventEmitter<void> = new EventEmitter<void>()
  @Input() folder: string = ""
  @Input() tracklets: string[] = []
  @Input() run: string = ""
  /*to make multi-selection easier and faster, if this is set to true clicking anywhere in the image will select it, instead of clicking the checkmark,
  @selectionMode is enabled when at least one image is selected anywhere in the application*/
  @Input() selectionMode: boolean = false
  @Input() start: string = ""
  @Input() end: string = ""
  @ViewChild('title') title: ElementRef | undefined
  @ViewChildren('trackletComponent') trackletComponent: QueryList<TrackletComponent> = new QueryList<TrackletComponent>()

  trackletsToImageNames: Map<string, Set<string>> = new Map<string, Set<string>>()
  selectedTracklets: Set<string> = new Set<string>();
  isHoveredFolder: boolean = false //will be used to show/hide the select check buttons
  imagesPerRow = 0
  imageWidth = 150 //px

  constructor(private service: BackendService) {
  }

  ngAfterViewInit() {
    this.imagesPerRow = Math.ceil(window.innerWidth / this.imageWidth) + 2
    this.loadImageNames()
  }

  loadImageNames() {
    this.service.getTrackletsToImageNamesMap(this.run, this.folder, this.start, this.end)
      .subscribe((trackletsToImages) => {
          Object.entries(trackletsToImages).forEach(([tracklet, images]) => {
            this.trackletsToImageNames.set(tracklet, new Set(images))
          })
          this.checkIfEmpty()
        },
        () => {
          console.log("Error loading folder " + this.folder)
          this.isEmpty.emit()
        })
  }

  deleteSelectedTracklets() {
    this.selectedTracklets.forEach(tracklet => this.trackletsToImageNames.delete(tracklet))
    this.deselectAllTracklets()
    this.checkIfEmpty()
  }

  toggleFolderSelect() {
    this.isAllTrackletsSelected() ? this.deselectAllTracklets() : this.selectAllTracklets()
    this.selectionChanged()
  }

  deselectAllTracklets() {
    this.trackletComponent.forEach(tracklet => tracklet.deselectTracklet())
    this.selectedTracklets.clear()
  }

  selectAllTracklets() {
    this.trackletsToImageNames.forEach((images, tracklet) => this.selectedTracklets.add(tracklet))
    this.trackletComponent.forEach(tracklet => tracklet.selectTracklet())
  }

  checkIfEmpty() {
    if (!this.trackletsToImageNames.size) this.isEmpty.emit()
  }

  getTracklets(): string[] {
    return Utils.getKeysFromMap(this.trackletsToImageNames)
  }

  getImagesByTracklet(tracklet: string): Set<string> {
    return this.trackletsToImageNames.get(tracklet) ?? new Set()
  }

  isAllTrackletsSelected() {
    return this.trackletsToImageNames.size && this.selectedTracklets.size === this.trackletsToImageNames.size
  }

  onTrackletSelectToggle(tracklet: string, selected: boolean) {
    selected ? this.selectedTracklets.add(tracklet) : this.selectedTracklets.delete(tracklet)
    this.selectionChanged()
  }

  //cloning the emitted Set to prevent it from being passed as a reference
  // and make sure all changes go through the event emitter
  selectionChanged() {
    this.onSelectionChange.emit(new Set([...this.selectedTracklets]))
  }
}
