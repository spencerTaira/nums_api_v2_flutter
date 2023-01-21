class Utils {
  dateFromDayOfYear(dayOfYear) {
    var day_of_year_to_month = {
            1: 1,
            32: 2,
            61: 3,
            92: 4,
            122: 5,
            153: 6,
            183: 7,
            214: 8,
            245: 9,
            275: 10,
            306: 11,
            336: 12,
        };
    var num;

    if (dayOfYear == 0) {
      num = 366;
    } else {
      num = dayOfYear;
    }

    List<int> firstOfEachMonth = day_of_year_to_month.keys.toList();
  
    for(int i = 0; i < firstOfEachMonth.length; i++){
      int first = firstOfEachMonth[i];
      int month = day_of_year_to_month[first]!;
      int day = num + 1 - first;

      if (num == first){
        return "${month}/1";
      }
      if (i == firstOfEachMonth.length-1){
        return "${month}/${day}";
      }
      if (dayOfYear > first && dayOfYear < firstOfEachMonth[i+1]){
        return "${month}/${day}";
      }
    }
  }
}