import 'package:flutter/material.dart';
import '../models/activity.dart';

class SensorService extends ChangeNotifier {
  int _stepCount = 0;
  int get stepCount => _stepCount;

  double _accelerometerMagnitude = 0.0;
  double get accelerometerMagnitude => _accelerometerMagnitude;

  bool _isTracking = false;
  bool get isTracking => _isTracking;

  // Симулируем данные (без реальных датчиков в эмуляторе)
  void startTracking() {
    _isTracking = true;
    notifyListeners();
  }

  void stopTracking() {
    _isTracking = false;
    notifyListeners();
  }

  void resetRoute() {
    _stepCount = 0;
    notifyListeners();
  }

  // Симуляция шага
  void simulateStep() {
    if (_isTracking) {
      _stepCount++;
      _accelerometerMagnitude = 7.5;
      notifyListeners();
    }
  }

  double calculateDistance() {
    // Среднее расстояние одного шага ≈ 0.75 м
    return (_stepCount * 0.75) / 1000;
  }

  // Определение типа активности по данным акселерометра
  ActivityType detectActivityType() {
    if (_accelerometerMagnitude < 3) {
      return ActivityType.gym;
    } else if (_accelerometerMagnitude < 6) {
      return ActivityType.walking;
    } else if (_accelerometerMagnitude < 10) {
      return ActivityType.running;
    } else {
      return ActivityType.cycling;
    }
  }

  // Расчёт калорий по MET-формуле (вес по умолчанию 75 кг)
  double calculateCalories(int steps, double distance, Duration duration) {
    double met;
    switch (detectActivityType()) {
      case ActivityType.walking:
        met = 3.5;
        break;
      case ActivityType.running:
        met = 8.0;
        break;
      case ActivityType.cycling:
        met = 6.0;
        break;
      case ActivityType.gym:
        met = 4.0;
        break;
    }
    const double weight = 75.0;
    final double hours = duration.inMinutes / 60.0;
    return weight * met * hours;
  }
}
