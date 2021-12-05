import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {Injectable} from "@angular/core";

export class Request {
  run: string | undefined
  folder: string | undefined
  start: string | undefined
  end: string | undefined
  destination: string | undefined
  mapping: any

  setStartEnd(start_h: string, start_m: string, end_h: string, end_m: string) {
    if (start_h && start_m && end_h && end_m) {
      this.start = start_h + ":" + start_m
      this.end = end_h + ":" + end_m
    }
  }
}

@Injectable()
export class HttpService {

  private static SERVICE_URL = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient) {
  }

  getFolders(run: string): Observable<any> {
    return this.http.get(HttpService.SERVICE_URL + `folder/${run}`)
  }

  getRuns(): Observable<string[]> {
    return this.http.get<string[]>(HttpService.SERVICE_URL + "runs")
  }

  getFolderContents(run: string, folder: string, start_h: string = '', start_m: string = '', end_h: string = '', end_m: string = ''): Observable<any> {
    let request = new Request();
    request.run = run
    request.folder = folder
    request.setStartEnd(start_h, start_m, end_h, end_m)
    return this.http.post(HttpService.SERVICE_URL + "images", request)
  }

  getImageSrc(run: string, folder: string, imageId: string): string {
    return HttpService.SERVICE_URL + `image/${run}/${folder}/${imageId}`
  }

  delete(run:string, folderToImages: Map<string, any>) : Observable<any> {
    let request = new Request();
    request.run = run
    request.mapping = {}
    folderToImages.forEach((value, key) => {
      request.mapping[key] = [...value]
    });
    return this.http.post(HttpService.SERVICE_URL + "delete", request)
  }
}
