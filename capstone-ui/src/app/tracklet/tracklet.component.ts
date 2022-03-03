import {
  AfterViewChecked,
  AfterViewInit, ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Host,
  Input,
  Output,
  ViewChild
} from '@angular/core';
import {BackendService} from "../service/backend.service";
import {DatePipe} from "@angular/common";
import {DragScrollComponent} from "ngx-drag-scroll";
import {FolderComponent} from "../folder/folder.component";
import {cache} from "../decorators/cache-decorator";
import {Utils} from "../utils/utils";

@Component({
  selector: 'app-tracklet',
  templateUrl: './tracklet.component.html',
  styleUrls: ['./tracklet.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TrackletComponent implements AfterViewInit, AfterViewChecked {

  @Input() imagesPerRow: number = 0
  @Input() tracklet: string = ''
  @Input() unloadedImages: Set<string> = new Set()  //all imageIDs in a folder, load image file as needed later and remove from this set
  @Output() onSelectionChange: EventEmitter<boolean> = new EventEmitter<boolean>()
  @ViewChild('images') dragScrollComponent: DragScrollComponent | undefined

  imageIdToImageMap: Map<string, any> = new Map<string, any>() //imageId to image file map
  isSelected: boolean = false
  DRAG_THRESHOLD: number = 0.8 //to load more items if user beyond (x*100)% of the folder content
  TIMESTAMP_FORMAT: string = 'HH:mm:ss SS'
  IMAGES_TIMEZONE = 'GMT'

  constructor(@Host() private parent: FolderComponent,
              private service: BackendService,
              private datePipe: DatePipe,
              private changeDetectorRef: ChangeDetectorRef) {
  }

  ngAfterViewChecked() {
    this.changeDetectorRef.detectChanges();
  }

  ngAfterViewInit() {
    this.loadFiles()
  }

  //Checks if horizontal scroll threshold has been reached, if so load more files
  onScroll() {
    let ref: any = this.dragScrollComponent?._contentRef
    const reachedScrollThreshold = ref.nativeElement.scrollLeft + ref.nativeElement.offsetWidth >= this.DRAG_THRESHOLD * ref.nativeElement.scrollWidth;
    if (reachedScrollThreshold) {
      this.loadFiles()
    }
  }

  //load as much images as the screen can fit
  loadFiles() {
    let loaded = 0
    for (let imageId of this.unloadedImages) {
      if (loaded >= this.imagesPerRow) break
      this.getImageFromService(imageId)
      loaded++
    }
  }

  getImageFromService(imageId: string) {
    let imageFile = new Image()
    imageFile.src = this.service.getImageSrc(this.parent.run, this.parent.folder, this.tracklet, imageId)
    this.unloadedImages.delete(imageId)
    this.imageIdToImageMap.set(imageId, imageFile)
  }

  toggleTrackletSelect() {
    this.isSelected ? this.deselectTracklet() : this.selectTracklet()
    this.selectionChanged()
  }

  deselectTracklet() {
    this.isSelected = false
  }

  selectionChanged() {
    this.onSelectionChange.emit(this.isSelected)
  }

  selectTracklet() {
    this.isSelected = true
  }

  @cache()
  getDate(imageId: string): string {
    let d: Date = new Date(parseInt(imageId.split(".")[0].split(";")[5]) / Math.pow(10, 6))
    return isNaN(d.getTime()) ? "Invalid timestamp" : this.datePipe.transform(d, this.TIMESTAMP_FORMAT, this.IMAGES_TIMEZONE) ?? ""
  }

  getImageNames(): string[] {
    return Utils.getKeysFromMap(this.imageIdToImageMap)
  }

  @cache()
  getImageFile(image: string) {
    return this.imageIdToImageMap.get(image)?.src
  }

}
