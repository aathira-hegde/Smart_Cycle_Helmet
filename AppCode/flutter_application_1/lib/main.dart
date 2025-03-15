import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:math';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Helmet App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Smart Helmet Dashboard'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  double _acceleration = 0.0;
  bool _alertActive = false;
  int _countdown = 30;
  Timer? _sensorTimer;
  Timer? _alertTimer;

  @override
  void initState() {
    super.initState();
    _startMockSensorData();
  }

  void _startMockSensorData() {
    _sensorTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _acceleration = Random().nextDouble() * 10; //note, this is fake data
        if (_acceleration > 7.0) {
          _startAlertCountdown();
        }
      });
    });
  }

  void _startAlertCountdown() {
    if (_alertActive) return;
    setState(() {
      _alertActive = true;
      _countdown = 30;
    });
    _alertTimer?.cancel();
    _alertTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_countdown > 0) {
        setState(() {
          _countdown--;
        });
      } else {
        timer.cancel();
        _sendEmergencyAlert();
      }
    });
  }

  void _sendEmergencyAlert() {
    print("Emergency alert sent to family members!");
  }

  void _cancelAlert() {
    setState(() {
      _alertActive = false;
    });
    _alertTimer?.cancel();
  }

  @override
  void dispose() {
    _sensorTimer?.cancel();
    _alertTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('Real-Time IMU Sensor Data:'),
            Text(
              'Acceleration: ${_acceleration.toStringAsFixed(2)} m/s²',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 30),
            if (_alertActive)
              Column(
                children: [
                  const Text(
                    'Alert! Crash detected.',
                    style: TextStyle(color: Colors.red, fontSize: 18),
                  ),
                  const SizedBox(height: 10),
                  Stack(
                    alignment: Alignment.center,
                    children: [
                      SizedBox(
                        width: 100,
                        height: 100,
                        child: CircularProgressIndicator(
                          value: _countdown / 30,
                          strokeWidth: 8,
                          color: Colors.red,
                        ),
                      ),
                      Text(
                        '$_countdown',
                        style: const TextStyle(
                          fontSize: 48,
                          fontWeight: FontWeight.bold,
                          color: Colors.red,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: _cancelAlert,
                    child: const Text('I am okay'),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
