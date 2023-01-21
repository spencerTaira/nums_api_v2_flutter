// To parse this JSON data, do
//
//     final welcome = welcomeFromJson(jsonString);
import 'dart:developer';
import 'dart:convert';

Welcome welcomeFromJson(String str) => Welcome.fromJson(json.decode(str));

class Welcome {
    Welcome({
        required this.fact,
    });

    Fact? fact;

    factory Welcome.fromJson(Map<String, dynamic> json) {
      print("In json");
      // print(Fact.fromJson(json["fact"]).fragment);
      if(json.containsKey("error")){
        return Welcome(
          fact: Fact.fromJson(json["error"]),
        );
      }
      print("In fact");
      return Welcome(
          fact: Fact.fromJson(json["fact"]),
      );
      // return Welcome(
      //   fact: Fact.fromJson(json["fact"]),
      // );
    }

}

// Math & Trivia
class Fact {
    Fact({
        this.fragment,
        this.number,
        this.statement,
        this.type,
    });

    String? fragment;
    String? number;
    String? statement;
    String? type;

    factory Fact.fromJson(Map<String, dynamic> json) {
      if(json.containsKey("message")){
        return Fact(
          statement: json["message"]
        );
      }
      if (json["type"] == "math" || json["type"] == "trivia"){
        return Fact(
          fragment: json["fragment"],
          number: json["number"].toString(),
          statement: json["statement"],
          type: json["type"],
        );
      } else if (json["type"] == "year"){
        return Fact(
          fragment: json["fragment"],
          number: json["year"].toString(),
          statement: json["statement"],
          type: '${json["type"]}s',
        );
      } else {
        return Fact(
          fragment: json["fragment"],
          number: '${json["month"]}/${json["day"]}',
          statement: json["statement"],
          type: '${json["type"]}s',
        );
      }
    }

    Map<String, dynamic> toJson() => {
        "fragment": fragment,
        "number": number,
        "statement": statement,
        "type": type,
    };
}


// ErrorHandler errorHandlerFromJson(String str) => ErrorHandler.fromJson(json.decode(str));

// // String errorHandlerToJson(ErrorHandler data) => json.encode(data.toJson());

// class ErrorHandler {
//     ErrorHandler({
//         required this.error,
//     });

//     Error? error;

//     factory ErrorHandler.fromJson(Map<String, dynamic> json) => ErrorHandler(
//         error: Error.fromJson(json["error"]),
//     );

// }

// class Error {
//     Error({
//         required this.message,
//         required this.status,
//     });

//     String message;
//     int status;

//     factory Error.fromJson(Map<String, dynamic> json) => Error(
//         message: json["message"],
//         status: json["status"],
//     );

//     Map<String, dynamic> toJson() => {
//         "message": message,
//         "status": status,
//     };
// }
