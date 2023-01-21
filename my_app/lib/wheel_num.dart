import 'package:flutter/material.dart';

class WheelNum extends StatelessWidget {
  int nums;

  WheelNum({required this.nums});

  @override
  Widget build(BuildContext context){
    return 
    // Padding(
    //   padding: const EdgeInsets.symmetric(vertical: 5.0),
    //   child: 
      Container(
        child: Center(
          child:Text(
            nums.toString(),
            style: TextStyle(
              fontSize:40,
              color: Colors.black,
              fontWeight: FontWeight.bold,
            ) //Text Style
          ) //Text
        ) //Center
      ); //Container
    // ); //Padding
  }
}