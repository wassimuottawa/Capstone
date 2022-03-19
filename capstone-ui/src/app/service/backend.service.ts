import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";
import {MatSnackBar} from "@angular/material/snack-bar";
import {tap} from "rxjs/operators";

export class Request {
  run: string | undefined
  folder: string | undefined
  start: string | undefined
  end: string | undefined
  destinationFolder: string | undefined
  mapping: any

  setStartEnd(start: string, end: string) {
    if (start && end) {
      this.start = start
      this.end = end
    }
  }
}

@Injectable()
export class BackendService {

  private static SERVICE_URL = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient, private _snackBar: MatSnackBar) {
  }

  getFoldersToTrackletsMap(run: string, start: string = '', end: string = ''): Observable<Object> {
    let request = new Request()
    request.run = run
    request.setStartEnd(start, end)
    return this.http.post<Map<string, string[]>>(BackendService.SERVICE_URL + `folders`, request)
  }

  getRuns(): Observable<string[]> {
    return this.http.get<string[]>(BackendService.SERVICE_URL + "runs")
  }

  getTrackletsToImageNamesMap(run: string, folder: string): Observable<Object> {
    let request = new Request();
    request.run = run
    request.folder = folder
    return this.http.post<Object>(BackendService.SERVICE_URL + "trackletsToImages", request)
  }

  getImageSrc(run: string, folder: string, tracklet: string, imageId: string): string {
    return BackendService.SERVICE_URL + `image/${run}/${folder}/${tracklet}/${imageId}`
  }

  mergeIntoNewFolder(run: string, folderToImages: Map<string, any>): Observable<any> {
    return this.http.post<string>(BackendService.SERVICE_URL + "merge", this.getMoveRequest(run, folderToImages))
      .pipe(tap(newFolder => this.openSnackbar(`Tracklets merged into folder ${newFolder}`)))
  }

  delete(run: string, folderToImages: Map<string, any>): Observable<any> {
    return this.http.post<any>(BackendService.SERVICE_URL + "delete", this.getMoveRequest(run, folderToImages))
      .pipe(tap(newFolder => this.openSnackbar(`Tracklet${folderToImages.size > 1 ? 's' : ''} deleted`)))
  }

  private getMoveRequest(run: string, folderToImages: Map<string, any>): Request {
    let request = new Request();
    request.run = run
    request.mapping = {}
    folderToImages.forEach((value, key) => request.mapping[key] = [...value]);
    return request
  }

  private openSnackbar(message: string) {
    this._snackBar.open(message, "Dismiss", {
      duration: 3000,
    })
  }
}
