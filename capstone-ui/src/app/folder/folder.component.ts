import {
  AfterViewChecked,
  AfterViewInit, ChangeDetectionStrategy,
  ChangeDetectorRef,
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
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FolderComponent implements AfterViewInit, AfterViewChecked {
  @Output() onSelectionChange: EventEmitter<Set<string>> = new EventEmitter<Set<string>>()
  @Output() isEmpty: EventEmitter<void> = new EventEmitter<void>()
  @Output() folderCollapsed: EventEmitter<void> = new EventEmitter<void>()
  @Input() folder: string = ""
  @Input() tracklets: string[] = []
  @Input() run: string = ""
  @ViewChild('title') title: ElementRef | undefined
  @ViewChildren('trackletComponent') trackletComponent: QueryList<TrackletComponent> = new QueryList<TrackletComponent>()

  trackletsToImageNames: Map<string, Set<string>> = new Map<string, Set<string>>()
  selectedTracklets: Set<string> = new Set<string>();
  /**
   * Will be calculated based on the width of the screen, this is used to know how many images to preload,
   * when user scrolls beyond {@link DRAG_THRESHOLD}, a count of {@link imagesPerRow} will be loaded more
   **/
  imagesPerRow = 0
  imageWidth = 150 //px

  constructor(private service: BackendService,
              private changeDetectorRef: ChangeDetectorRef) {
  }

  ngAfterViewInit() {
    this.imagesPerRow = Math.ceil(window.innerWidth / this.imageWidth) + 2
    this.loadImageNames()
  }

  loadImageNames() {
    this.service.getTrackletsToImageNamesMap(this.run, this.folder)
      .subscribe((trackletsToImages) => {
          Object.entries(trackletsToImages).forEach(([tracklet, images]) => {
            this.trackletsToImageNames.set(tracklet, new Set(images))
          })
          this.deselectAllTracklets()
          this.checkIfEmpty()
        },
        () => {
          console.log("Error loading folder " + this.folder)
          this.isEmpty.emit()
        })
  }

  ngAfterViewChecked() {
    this.changeDetectorRef.detectChanges();
  }

  deleteSelectedTracklets() {
    if (this.isAllTrackletsSelected()) this.isEmpty.emit()
    else {
      this.selectedTracklets.forEach(tracklet => this.trackletsToImageNames.delete(tracklet))
      this.deselectAllTracklets()
      this.checkIfEmpty()
    }
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
  //and make sure all changes go through the event emitter
  selectionChanged() {
    this.onSelectionChange.emit(new Set([...this.selectedTracklets]))
  }
}
