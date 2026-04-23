import 'package:flutter/material.dart';
import '../models/activity.dart';
import '../services/database_service.dart';

class ActivityProvider extends ChangeNotifier {
  final DatabaseService _db = DatabaseService();

  List<ActivityRecord> _activities = [];
  List<ActivityRecord> get activities => _activities;

  ActivityRecord? _currentActivity;
  ActivityRecord? get currentActivity => _currentActivity;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String? _error;
  String? get error => _error;

  ActivityProvider() {
    loadActivities();
  }

  Future<void> loadActivities() async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    try {
      _activities = await _db.getAllActivities();
    } catch (e) {
      _error = 'Ошибка загрузки: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> saveActivity(ActivityRecord activity) async {
    try {
      await _db.insertActivity(activity);
      _activities.insert(0, activity);
      _activities.sort((a, b) => b.startTime.compareTo(a.startTime));
    } catch (e) {
      _error = 'Ошибка сохранения: $e';
    }
    notifyListeners();
  }

  Future<void> deleteActivity(String id) async {
    try {
      await _db.deleteActivity(id);
      _activities.removeWhere((a) => a.id == id);
    } catch (e) {
      _error = 'Ошибка удаления: $e';
    }
    notifyListeners();
  }

  void startNewActivity(ActivityType type) {
    _currentActivity = ActivityRecord(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      type: type,
      startTime: DateTime.now(),
      steps: 0,
      distance: 0.0,
      calories: 0.0,
    );
    notifyListeners();
  }

  void updateCurrentActivity({int? steps, double? distance, double? calories}) {
    if (_currentActivity == null) return;
    _currentActivity = ActivityRecord(
      id: _currentActivity!.id,
      type: _currentActivity!.type,
      startTime: _currentActivity!.startTime,
      steps: steps ?? _currentActivity!.steps,
      distance: distance ?? _currentActivity!.distance,
      calories: calories ?? _currentActivity!.calories,
    );
    notifyListeners();
  }

  Future<void> finishCurrentActivity() async {
    if (_currentActivity == null) return;
    final completed = ActivityRecord(
      id: _currentActivity!.id,
      type: _currentActivity!.type,
      startTime: _currentActivity!.startTime,
      endTime: DateTime.now(),
      steps: _currentActivity!.steps,
      distance: _currentActivity!.distance,
      calories: _currentActivity!.calories,
    );
    await saveActivity(completed);
    _currentActivity = null;
    notifyListeners();
  }
}
