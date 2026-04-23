import 'dart:convert';
import 'package:flutter/material.dart';

enum ActivityType {
  walking,
  running,
  cycling,
  gym;

  String get displayName {
    switch (this) {
      case ActivityType.walking: return 'Ходьба';
      case ActivityType.running: return 'Бег';
      case ActivityType.cycling: return 'Велосипед';
      case ActivityType.gym: return 'Тренажерный зал';
    }
  }

  IconData get icon {
    switch (this) {
      case ActivityType.walking: return Icons.directions_walk;
      case ActivityType.running: return Icons.directions_run;
      case ActivityType.cycling: return Icons.directions_bike;
      case ActivityType.gym: return Icons.fitness_center;
    }
  }

  Color get color {
    switch (this) {
      case ActivityType.walking: return Colors.green;
      case ActivityType.running: return Colors.orange;
      case ActivityType.cycling: return Colors.blue;
      case ActivityType.gym: return Colors.purple;
    }
  }
}

class LatLng {
  final double latitude;
  final double longitude;
  LatLng(this.latitude, this.longitude);
  Map<String, dynamic> toJson() => {'lat': latitude, 'lng': longitude};
  factory LatLng.fromJson(Map<String, dynamic> json) =>
      LatLng(json['lat'], json['lng']);
}

class ActivityRecord {
  final String id;
  final ActivityType type;
  final DateTime startTime;
  final DateTime? endTime;
  final int steps;
  final double distance;
  final double calories;
  final double? averageHeartRate;
  final List<LatLng>? route;

  ActivityRecord({
    required this.id,
    required this.type,
    required this.startTime,
    this.endTime,
    required this.steps,
    required this.distance,
    required this.calories,
    this.averageHeartRate,
    this.route,
  });

  Duration get duration {
    if (endTime == null) return Duration.zero;
    return endTime!.difference(startTime);
  }

  // Темп: минуты на километр
  double get pace {
    if (distance == 0 || duration.inMinutes == 0) return 0;
    return duration.inMinutes / distance;
  }

  Map<String, dynamic> toMap() => {
    'id': id,
    'type': type.index,
    'startTime': startTime.millisecondsSinceEpoch,
    'endTime': endTime?.millisecondsSinceEpoch,
    'steps': steps,
    'distance': distance,
    'calories': calories,
    'averageHeartRate': averageHeartRate,
    'route': route != null
        ? jsonEncode(route!.map((p) => p.toJson()).toList())
        : null,
  };

  factory ActivityRecord.fromMap(Map<String, dynamic> map) => ActivityRecord(
    id: map['id'],
    type: ActivityType.values[map['type']],
    startTime: DateTime.fromMillisecondsSinceEpoch(map['startTime']),
    endTime: map['endTime'] != null
        ? DateTime.fromMillisecondsSinceEpoch(map['endTime'])
        : null,
    steps: map['steps'],
    distance: map['distance'],
    calories: map['calories'],
    averageHeartRate: map['averageHeartRate'],
    route: map['route'] != null
        ? (jsonDecode(map['route']) as List)
            .map((p) => LatLng.fromJson(p))
            .toList()
        : null,
  );
}
