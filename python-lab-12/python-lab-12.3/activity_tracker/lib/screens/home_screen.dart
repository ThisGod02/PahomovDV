import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/activity_provider.dart';
import '../providers/theme_provider.dart';
import '../models/activity.dart';
import '../widgets/activity_card.dart';
import '../widgets/progress_ring.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Activity Tracker'),
        actions: [
          Consumer<ThemeProvider>(
            builder: (context, tp, _) => IconButton(
              icon: Icon(tp.isDarkMode ? Icons.light_mode : Icons.dark_mode),
              onPressed: tp.toggleTheme,
            ),
          ),
        ],
      ),
      body: Consumer2<ActivityProvider, SensorProvider>(
        builder: (context, activityProvider, sensorProvider, _) {
          if (activityProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (activityProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(activityProvider.error!, style: const TextStyle(color: Colors.red)),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: activityProvider.loadActivities,
                    child: const Text('Повторить'),
                  ),
                ],
              ),
            );
          }
          if (activityProvider.currentActivity != null) {
            return _buildCurrentActivity(context, activityProvider.currentActivity!, sensorProvider);
          }
          return _buildActivitiesList(context, activityProvider);
        },
      ),
      floatingActionButton: Consumer<ActivityProvider>(
        builder: (context, provider, _) {
          return FloatingActionButton(
            onPressed: provider.currentActivity != null
                ? () => _finishActivity(context)
                : () => _showStartDialog(context),
            child: Icon(provider.currentActivity != null ? Icons.stop : Icons.play_arrow),
          );
        },
      ),
    );
  }

  Widget _buildCurrentActivity(BuildContext context, ActivityRecord activity, SensorProvider sensorProvider) {
    final stepGoal = 10000;
    final progress = (sensorProvider.stepCount / stepGoal).clamp(0.0, 1.0);

    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Анимированное кольцо прогресса
          ProgressRing(
            progress: progress,
            size: 160,
            color: activity.type.color,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  '${sensorProvider.stepCount}',
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                ),
                const Text('шагов', style: TextStyle(fontSize: 12)),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Text(activity.type.displayName,
              style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _stat(context, 'Шаги', sensorProvider.stepCount.toString(), Icons.directions_walk),
              _stat(context, 'км', sensorProvider.calculateDistance().toStringAsFixed(2), Icons.straighten),
            ],
          ),
          const SizedBox(height: 16),
          // Симуляция шага (для демо)
          ElevatedButton.icon(
            onPressed: () => sensorProvider.simulateStep(),
            icon: const Icon(Icons.directions_walk),
            label: const Text('Симулировать шаг'),
          ),
        ],
      ),
    );
  }

  Widget _stat(BuildContext context, String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: Colors.blue),
        const SizedBox(height: 4),
        Text(value, style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
        Text(label, style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }

  Widget _buildActivitiesList(BuildContext context, ActivityProvider provider) {
    if (provider.activities.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.fitness_center, size: 64, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text('Нет тренировок', style: Theme.of(context).textTheme.titleLarge?.copyWith(color: Colors.grey)),
            const SizedBox(height: 8),
            Text('Нажмите ▶ чтобы начать', style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey)),
          ],
        ),
      );
    }
    return ListView.builder(
      itemCount: provider.activities.length,
      itemBuilder: (context, index) {
        final activity = provider.activities[index];
        return ActivityCard(
          activity: activity,
          onDelete: () => _confirmDelete(context, activity),
        );
      },
    );
  }

  void _showStartDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Новая тренировка'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: ActivityType.values.map((type) {
            return ListTile(
              leading: Icon(type.icon, color: type.color),
              title: Text(type.displayName),
              onTap: () {
                Navigator.pop(ctx);
                final provider = Provider.of<ActivityProvider>(context, listen: false);
                final sensor = Provider.of<SensorProvider>(context, listen: false);
                provider.startNewActivity(type);
                sensor.startTracking();
              },
            );
          }).toList(),
        ),
      ),
    );
  }

  void _finishActivity(BuildContext context) async {
    final provider = Provider.of<ActivityProvider>(context, listen: false);
    final sensor = Provider.of<SensorProvider>(context, listen: false);
    provider.updateCurrentActivity(
      steps: sensor.stepCount,
      distance: sensor.calculateDistance(),
    );
    await provider.finishCurrentActivity();
    sensor.stopTracking();
    sensor.resetRoute();
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Тренировка сохранена ✓')),
      );
    }
  }

  void _confirmDelete(BuildContext context, ActivityRecord activity) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Удалить тренировку?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Отмена')),
          TextButton(
            onPressed: () {
              Provider.of<ActivityProvider>(context, listen: false).deleteActivity(activity.id);
              Navigator.pop(ctx);
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Удалить'),
          ),
        ],
      ),
    );
  }
}
