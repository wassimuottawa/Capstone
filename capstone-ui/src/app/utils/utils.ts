export class Utils {
  public static equalTuples(tup1: [string, string], tup2: [string, string]): boolean {
    return tup1[0] == tup2[0] && tup1[1] == tup2[1]
  }
}
