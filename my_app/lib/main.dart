
import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:my_app/api_service.dart';
import 'package:my_app/json.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'wheel_num.dart';
import 'utils.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        title: 'Namer App',
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        ),
        home: MyHomePage(),
      ),
    );
  }
}

class MyAppState extends ChangeNotifier {
  var current = WordPair.random();

  void getNext() {
    current = WordPair.random();
    notifyListeners();
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var appState = context.watch<MyAppState>();
    var pair = appState.current;

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            APIWidget(),
          ],
        ),
      ),
    );
  }
}

class APIWidget extends StatefulWidget {
  const APIWidget({super.key});

  @override
  State<APIWidget> createState() => APIWidgetState();
}

class APIWidgetState extends State<APIWidget> {
  late Fact? fact;
  var facts = <Fact?>[];
  Fact? numWheelFact;
  var thousands = 0;
  var hundreds = 0;
  var tens = 0;
  var ones = 0;
  var category = 'math';
  var number = '0';


  @override
  void initState() {
    super.initState();
    getInitFactAPI();
    print('INIT FACTS');
    print(facts);
  }

  void isDate() {
    if (category == "dates") {
      var dayOfYear = int.parse('$thousands$hundreds$tens$ones') % 366;
      number = Utils().dateFromDayOfYear(dayOfYear);
    } else {
      number = '$thousands$hundreds$tens$ones'.replaceFirst(new RegExp(r'^0+'), '');
      if (number == "") number = '0';
    }

    setState(() {
      number = number;
    });
  }

  void getInitFactAPI() async {
    fact = (await ApiService().getFact('/math/5'));
    facts.add(fact);
    fact = (await ApiService().getFact('/trivia/42'));
    numWheelFact = fact;
    facts.add(fact);
    fact = (await ApiService().getFact('/years/2019'));
    facts.add(fact);
    fact = (await ApiService().getFact('/dates/4/20'));
    facts.add(fact);

    setState(() {
      facts = facts;
      numWheelFact = numWheelFact;
    });
  }

  void getFactAPI(endpoint) async {
    fact = (await ApiService().getFact(endpoint));
    print("getFactAPI#######################");
    print(fact);
    setState(() {
      numWheelFact = fact;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center ,
      children: [
        CarouselWithIndicatorDemo(facts:facts),
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    category = "math";
                  });
                  isDate();
                },
                child: Text("Math"),
              ),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    category = "trivia";
                  });
                  isDate();
                },
                child: Text("Trivia"),
              ),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    category = "years";
                  });
                  isDate();
                },
                child: Text("Year"),
              ),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    category = "dates";
                  });
                  isDate();
                },
                child: Text("Date"),
              ),
            ],
          ),
        ),
        SizedBox(height: 5),
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: Container(
              height: 100,
              child:
                Row(
                  mainAxisAlignment:MainAxisAlignment.center,
                  children: [
                    Container(
                      width: 30,
                      child:
                        ListWheelScrollView.useDelegate(
                          itemExtent:45,
                          perspective: 0.005,
                          diameterRatio: 1.2,
                          physics: FixedExtentScrollPhysics(),
                          onSelectedItemChanged: (ind) {
                            setState(() {
                              thousands = ind;
                            });
                            isDate();
                          },
                          childDelegate:
                            ListWheelChildLoopingListDelegate(
                              children: List<Widget>.generate(
                                10, (index) => WheelNum(nums:index),
                            )
                          )
                        )
                    ),
                    Container(
                      width: 30,
                      child:
                        ListWheelScrollView.useDelegate(
                          itemExtent:45,
                          perspective: 0.005,
                          diameterRatio: 1.2,
                          physics: FixedExtentScrollPhysics(),
                          onSelectedItemChanged: (ind) {
                            setState(() {
                              hundreds = ind;
                            });
                            isDate();
                          },
                          childDelegate:
                            ListWheelChildLoopingListDelegate(
                              children: List<Widget>.generate(
                                10, (index) => WheelNum(nums:index),

                            )
                          )
                        )
                    ),
                    Container(
                      width: 30,
                      child:
                        ListWheelScrollView.useDelegate(
                          itemExtent:45,
                          perspective: 0.005,
                          diameterRatio: 1.2,
                          physics: FixedExtentScrollPhysics(),
                          onSelectedItemChanged: (ind) {
                            setState(() {
                              tens = ind;
                            });
                            isDate();
                          },
                          childDelegate:
                            ListWheelChildLoopingListDelegate(
                              children: List<Widget>.generate(
                                10, (index) => WheelNum(nums:index),

                            )
                          )
                        )
                    ),
                    Container(
                      width: 30,
                      child:
                        ListWheelScrollView.useDelegate(
                          itemExtent:45,
                          perspective: 0.005,
                          diameterRatio: 1.2,
                          physics: FixedExtentScrollPhysics(),
                          onSelectedItemChanged: (ind) {
                            setState(() {
                              ones = ind;
                            });
                            isDate();
                          },
                          childDelegate:
                            ListWheelChildLoopingListDelegate(
                              children: List<Widget>.generate(
                                10, (index) => WheelNum(nums:index),

                            )
                          )
                        )
                    ),
                  ]
                )
            ),
          ),
          Text(
            'numbersapi.com/${category}/${number}'
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: () {
                  getFactAPI('/${category}/${number}');
                },
                child: Text('Get Fact'),
              ),
              ElevatedButton(
                onPressed: () {
                  getFactAPI('/${category}/random');
                  setState(() {
                    number = 'random';
                  });
                },
                child: Text('Get Random'),
              ),
            ]
          ),
        Text('${numWheelFact?.statement}'), //Container
      ],
    );
  }
}

class BigCard extends StatelessWidget {
  const BigCard({
    Key? key,
    required this.pair,
  }) : super(key: key);

  final WordPair pair;

  @override
  Widget build(BuildContext context) {
    var theme = Theme.of(context);
    var style = theme.textTheme.displayMedium!.copyWith(
      color: theme.colorScheme.onPrimary,
    );

    return Card(
      color: theme.colorScheme.primary,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Text(pair.asLowerCase, style: style),
      ),
    );
  }
}

// // ################# Carousel ############################
class CarouselWithIndicatorDemo extends StatefulWidget {
  final List<Fact?> facts;

  const CarouselWithIndicatorDemo({
    required this.facts,
  });

  @override
  State<StatefulWidget> createState() => _CarouselWithIndicatorState(facts:facts);

}

class _CarouselWithIndicatorState extends State<CarouselWithIndicatorDemo> {
  int _current = 0;
  final List<Fact?> facts;

  _CarouselWithIndicatorState({
    required this.facts,
  });

  final CarouselController _controller = CarouselController();

  @override
  void initState() {
    super.initState();
    print('Carousel State');
    print(facts);
  }

 @override
  Widget build(BuildContext context) => Column(
    children: <Widget>[
      CarouselSlider(
          items: facts.map((fact) {
            return Builder(
              builder: (BuildContext context) {
                return Container(
                  width: MediaQuery.of(context).size.width,
                  margin: EdgeInsets.symmetric(horizontal: 5.0),
                  decoration: BoxDecoration(
                    color: Colors.amber
                  ),
                  child: Column(children: [
                    Text('${fact?.type}', style: TextStyle(fontSize: 16.0),),
                    Text('numbersapi.com/${fact?.type}/${fact?.number}',
                          style: TextStyle(fontSize: 16.0),),
                    Text('${fact?.statement}', style: TextStyle(fontSize: 16.0),),
                  ])
                );
              },
            );
          }).toList(),
          options: CarouselOptions(
              height: 200,
              viewportFraction: 0.8,
              initialPage: 0,
              enableInfiniteScroll: true,
              reverse: false,
              autoPlay: true,
              autoPlayInterval: Duration(seconds: 3),
              autoPlayAnimationDuration: Duration(milliseconds: 800),
              autoPlayCurve: Curves.fastOutSlowIn,
              enlargeCenterPage: true,
              enlargeFactor: 0.3,
              scrollDirection: Axis.horizontal,
              onPageChanged: (index, reason) {
                  setState(() {
                    _current = index;
                  });
                }),
          ),
      Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: facts.asMap().entries.map((entry) {
            return GestureDetector(
              onTap: () => _controller.animateToPage(entry.key),
              child: Container(
                width: 12.0,
                height: 12.0,
                margin: EdgeInsets.symmetric(vertical: 8.0, horizontal: 4.0),
                decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: (Theme.of(context).brightness == Brightness.dark
                            ? Colors.white
                            : Colors.black)
                        .withOpacity(_current == entry.key ? 0.9 : 0.4)),
              ),
            );
          }).toList(),
      ),
    ]
  );
}
