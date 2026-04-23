import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/activity.dart';

class ActivityCard extends StatelessWidget {
  final ActivityRecord activity;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;

  const ActivityCard({Key? key, required this.activity, this.onTap, this.onDelete})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final dateStr = DateFormat('dd MMM yyyy, HH:mm').format(activity.startTime);
    final durMin = activity.duration.inMinutes;
    final durStr = '${durMin ~/ 60}ч ${durMin % 60}мин';

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: activity.type.color.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(activity.type.icon, color: activity.type.color),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(activity.type.displayName,
                            style: theme.textTheme.titleMedium
                                ?.copyWith(fontWeight: FontWeight.bold)),
                        Text(dateStr, style: theme.textTheme.bodySmall),
                      ],
                    ),
                  ),
                  if (onDelete != null)
                    IconButton(
                        icon: const Icon(Icons.delete_outline, color: Colors.grey),
                        onPressed: onDelete),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _stat(Icons.timer, durStr, 'Длит.'),
                  _stat(Icons.directions_walk, activity.steps.toString(), 'Шаги'),
                  _stat(Icons.straighten, '${activity.distance.toStringAsFixed(2)} км', 'Дист.'),
                  _stat(Icons.local_fire_department, '${activity.calories.toStringAsFixed(0)} ккал', 'Кал.'),
                ],
              ),
              // Индикатор маршрута
              if (activity.route != null && activity.route!.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Row(
                    children: [
                      Icon(Icons.route, size: 14, color: Colors.grey[600]),
                      const SizedBox(width: 4),
                      Text('Маршрут: ${activity.route!.length} точек',
                          style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _stat(IconData icon, String value, String label) => Column(
    children: [
      Icon(icon, size: 16, color: Colors.grey),
      const SizedBox(height: 2),
      Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
      Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
    ],
  );
}
