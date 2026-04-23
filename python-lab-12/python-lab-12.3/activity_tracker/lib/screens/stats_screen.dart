import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/activity_provider.dart';

class StatsScreen extends StatelessWidget {
  const StatsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Статистика')),
      body: Consumer<ActivityProvider>(
        builder: (context, provider, _) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          final acts = provider.activities;
          int totalSteps = 0;
          double totalDist = 0;
          int totalCal = 0;
          for (var a in acts) {
            totalSteps += a.steps;
            totalDist += a.distance;
            totalCal += a.calories.toInt();
          }

          // Данные за последние 7 дней
          final now = DateTime.now();
          final weekData = List.generate(7, (i) {
            final day = DateTime(now.year, now.month, now.day - (6 - i));
            final daySteps = acts
                .where((a) =>
                    a.startTime.year == day.year &&
                    a.startTime.month == day.month &&
                    a.startTime.day == day.day)
                .fold(0, (sum, a) => sum + a.steps);
            return MapEntry(day, daySteps);
          });
          final maxSteps = weekData.map((e) => e.value).fold(0, (a, b) => a > b ? a : b);

          return SingleChildScrollView(
            child: Column(
              children: [
                // Карточки общей статистики
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.5,
                    children: [
                      _statCard(context, 'Шаги', '$totalSteps', Icons.directions_walk, Colors.blue),
                      _statCard(context, 'Дистанция', '${totalDist.toStringAsFixed(2)} км', Icons.straighten, Colors.green),
                      _statCard(context, 'Калории', '$totalCal', Icons.local_fire_department, Colors.orange),
                      _statCard(context, 'Тренировки', '${acts.length}', Icons.fitness_center, Colors.purple),
                    ],
                  ),
                ),

                // График активности за 7 дней (гистограмма)
                Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Шаги за последние 7 дней',
                            style: Theme.of(context).textTheme.titleMedium),
                        const SizedBox(height: 16),
                        SizedBox(
                          height: 120,
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: weekData.map((entry) {
                              final frac = maxSteps > 0 ? entry.value / maxSteps : 0.0;
                              return Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(horizontal: 3),
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.end,
                                    children: [
                                      Flexible(
                                        child: FractionallySizedBox(
                                          heightFactor: frac.toDouble(),
                                          child: Container(
                                            decoration: BoxDecoration(
                                              color: Colors.blue,
                                              borderRadius: BorderRadius.circular(4),
                                            ),
                                          ),
                                        ),
                                      ),
                                      const SizedBox(height: 4),
                                      Text('${entry.key.day}/${entry.key.month}',
                                          style: const TextStyle(fontSize: 8)),
                                    ],
                                  ),
                                ),
                              );
                            }).toList(),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _statCard(BuildContext ctx, String label, String value, IconData icon, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 4),
            Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: color)),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
