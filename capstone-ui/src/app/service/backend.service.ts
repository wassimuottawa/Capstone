import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";

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

  constructor(private http: HttpClient) {
  }

  getFolders(run: string): Observable<any> {
    return this.http.get<string[]>(BackendService.SERVICE_URL + `folder/${run}`)
  }

  getRuns(): Observable<string[]> {
    return this.http.get<string[]>(BackendService.SERVICE_URL + "runs")
  }

  getFolderContents(run: string, folder: string, start: string = '', end: string = ''): Observable<any> {
    let request = new Request();
    request.run = run
    request.folder = folder
    request.setStartEnd(start, end)
    return this.http.post<string[]>(BackendService.SERVICE_URL + "images", request)
  }

  getImageSrc(run: string, folder: string, imageId: string): string {
    return BackendService.SERVICE_URL + `image/${run}/${folder}/${imageId}`
  }

  delete(run: string, folderToImages: Map<string, any>): Observable<any> {
    let request = new Request();
    request.run = run
    request.mapping = {}
    folderToImages.forEach((value, key) => request.mapping[key] = [...value]);
    return this.http.post<any>(BackendService.SERVICE_URL + "delete", request)
  }
}
