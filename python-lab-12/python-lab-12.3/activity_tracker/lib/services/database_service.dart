import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/activity.dart';
import '../models/user_stats.dart';

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'activity_tracker.db');
    return await openDatabase(path, version: 1, onCreate: _onCreate);
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE activities(
        id TEXT PRIMARY KEY,
        type INTEGER NOT NULL,
        startTime INTEGER NOT NULL,
        endTime INTEGER,
        steps INTEGER NOT NULL,
        distance REAL NOT NULL,
        calories REAL NOT NULL,
        averageHeartRate REAL,
        route TEXT
      )
    ''');
    await db.execute('''
      CREATE TABLE daily_stats(
        date INTEGER PRIMARY KEY,
        steps INTEGER NOT NULL,
        distance REAL NOT NULL,
        calories INTEGER NOT NULL,
        workouts INTEGER NOT NULL
      )
    ''');
  }

  Future<void> insertActivity(ActivityRecord activity) async {
    final db = await database;
    await db.insert('activities', activity.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<List<ActivityRecord>> getAllActivities() async {
    final db = await database;
    final maps = await db.query('activities', orderBy: 'startTime DESC');
    return maps.map((m) => ActivityRecord.fromMap(m)).toList();
  }

  Future<List<ActivityRecord>> getActivitiesByDate(DateTime date) async {
    final db = await database;
    final start = DateTime(date.year, date.month, date.day);
    final end = start.add(const Duration(days: 1));
    final maps = await db.query(
      'activities',
      where: 'startTime >= ? AND startTime < ?',
      whereArgs: [start.millisecondsSinceEpoch, end.millisecondsSinceEpoch],
      orderBy: 'startTime DESC',
    );
    return maps.map((m) => ActivityRecord.fromMap(m)).toList();
  }

  Future<void> deleteActivity(String id) async {
    final db = await database;
    await db.delete('activities', where: 'id = ?', whereArgs: [id]);
  }

  Future<UserStats> getUserStats() async {
    final db = await database;
    final maps = await db.query('activities');

    int totalSteps = 0;
    double totalDistance = 0.0;
    int totalCalories = 0;
    double totalPace = 0.0;

    for (var map in maps) {
      totalSteps += map['steps'] as int;
      totalDistance += map['distance'] as double;
      totalCalories += (map['calories'] as double).toInt();
      if (map['endTime'] != null) {
        final dur = DateTime.fromMillisecondsSinceEpoch(map['endTime'] as int)
            .difference(DateTime.fromMillisecondsSinceEpoch(map['startTime'] as int));
        if (dur.inMinutes > 0 && (map['distance'] as double) > 0) {
          totalPace += dur.inMinutes / (map['distance'] as double);
        }
      }
    }

    return UserStats(
      totalSteps: totalSteps,
      totalDistance: totalDistance,
      totalCalories: totalCalories,
      totalWorkouts: maps.length,
      averagePace: maps.isNotEmpty ? totalPace / maps.length : 0,
    );
  }
}
