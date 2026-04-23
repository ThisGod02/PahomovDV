import 'package:flutter/material.dart';

class ThemeProvider extends ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.system;
  ThemeMode get themeMode => _themeMode;

  bool get isDarkMode => _themeMode == ThemeMode.dark;

  void toggleTheme() {
    _themeMode =
        _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }
}

class SensorProvider extends ChangeNotifier {
  // Псевдоним для sensor_service без нативных зависимостей
  double _accelerometerMagnitude = 0.0;
  double get accelerometerMagnitude => _accelerometerMagnitude;
  int _stepCount = 0;
  int get stepCount => _stepCount;
  bool _isTracking = false;
  bool get isTracking => _isTracking;

  void startTracking() { _isTracking = true; notifyListeners(); }
  void stopTracking() { _isTracking = false; notifyListeners(); }
  void resetRoute() { _stepCount = 0; notifyListeners(); }
  void simulateStep() {
    if (_isTracking) { _stepCount++; _accelerometerMagnitude = 7.5; notifyListeners(); }
  }
  double calculateDistance() => (_stepCount * 0.75) / 1000;
}

class AppThemes {
  static ThemeData get lightTheme => ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
    brightness: Brightness.light,
    useMaterial3: true,
    cardTheme: CardTheme(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  );

  static ThemeData get darkTheme => ThemeData(
    colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue, brightness: Brightness.dark),
    brightness: Brightness.dark,
    useMaterial3: true,
    cardTheme: CardTheme(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
  );
}
