import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:my_app/constants.dart';
import 'package:my_app/json.dart';

class ApiService {
  Future<Fact?> getFact(endpoint) async {
    try {
      var url = Uri.parse(ApiConstants.baseUrl + endpoint);
      var response = await http.get(url);
      if (response.statusCode == 200) {
        print('200 status code');
        print(response.body);
        Welcome fact = welcomeFromJson(response.body);
        print('factory');
        print(fact.fact);
        return fact.fact;
      }
      print('not 200 status code');
      print(response.body);
      Welcome fact = welcomeFromJson(response.body);

      return fact.fact;
    } catch (e) {
      log(e.toString());
    }

    return null;
  }
}