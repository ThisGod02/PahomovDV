import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/activity.dart';

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
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
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
  }
  
  Future<void> insertActivity(ActivityRecord activity) async {
    final db = await database;
    await db.insert('activities', activity.toMap(), conflictAlgorithm: ConflictAlgorithm.replace);
  }
  
  Future<List<ActivityRecord>> getAllActivities() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('activities', orderBy: 'startTime DESC');
    return List.generate(maps.length, (i) => ActivityRecord.fromMap(maps[i]));
  }

  Future<void> deleteActivity(String id) async {
    final db = await database;
    await db.delete('activities', where: 'id = ?', whereArgs: [id]);
  }
}
