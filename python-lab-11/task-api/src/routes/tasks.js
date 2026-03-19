const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const { 
  validateCreateTask, 
  validateUpdateTask, 
  validateId 
} = require('../middleware/validation');
const { 
  initializeDataFile, 
  readData, 
  writeData, 
  getNextId 
} = require('../utils/fileOperations');

// Инициализация файла данных при запуске
initializeDataFile();

// GET /api/tasks - получение всех задач с фильтрацией
router.get('/', async (req, res, next) => {
  try {
    const { category, completed, priority, sortBy, page = 1, limit = 10 } = req.query;
    const data = await readData();
    
    let tasks = [...data.tasks];
    
    // Фильтрация по категории
    if (category) {
      tasks = tasks.filter(t => t.category === category);
    }
    
    // Фильтрация по статусу выполнения
    if (completed !== undefined) {
      const isCompleted = completed === 'true';
      tasks = tasks.filter(t => t.completed === isCompleted);
    }
    
    // Фильтрация по приоритету
    if (priority) {
      tasks = tasks.filter(t => t.priority === parseInt(priority));
    }
    
    // Сортировка
    if (sortBy) {
      const direction = sortBy.startsWith('-') ? -1 : 1;
      const field = sortBy.startsWith('-') ? sortBy.substring(1) : sortBy;
      
      tasks.sort((a, b) => {
        if (a[field] < b[field]) return -1 * direction;
        if (a[field] > b[field]) return 1 * direction;
        return 0;
      });
    }
    
    // Пагинация
    const startIndex = (parseInt(page) - 1) * parseInt(limit);
    const paginatedTasks = tasks.slice(startIndex, startIndex + parseInt(limit));
    
    res.json({
      success: true,
      count: tasks.length,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total: tasks.length
      },
      data: paginatedTasks
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/stats/summary - статистика по задачам (ставим выше /:id чтобы не было конфликта)
router.get('/stats/summary', async (req, res, next) => {
  try {
    const data = await readData();
    const tasks = data.tasks;
    
    const now = new Date();
    const stats = {
      total: tasks.length,
      completed: tasks.filter(t => t.completed).length,
      pending: tasks.filter(t => !t.completed).length,
      overdue: tasks.filter(t => !t.completed && t.dueDate && new Date(t.dueDate) < now).length,
      byCategory: {},
      byPriority: {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0
      }
    };
    
    tasks.forEach(t => {
      // По категориям
      stats.byCategory[t.category] = (stats.byCategory[t.category] || 0) + 1;
      // По приоритетам
      if (stats.byPriority[t.priority] !== undefined) {
        stats.byPriority[t.priority]++;
      }
    });
    
    res.json({
      success: true,
      data: stats
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/search/text - поиск задач
router.get('/search/text', async (req, res, next) => {
  try {
    const { q } = req.query;
    
    if (!q || q.trim().length < 2) {
      return res.status(400).json({
        success: false,
        error: 'Поисковый запрос должен содержать минимум 2 символа'
      });
    }
    
    const data = await readData();
    const searchTerm = q.toLowerCase().trim();
    
    const results = data.tasks.filter(t => 
      t.title.toLowerCase().includes(searchTerm) || 
      (t.description && t.description.toLowerCase().includes(searchTerm))
    );
    
    res.json({
      success: true,
      count: results.length,
      data: results
    });
    
  } catch (error) {
    next(error);
  }
});

// GET /api/tasks/:id - получение задачи по ID
router.get('/:id', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    const task = data.tasks.find(t => t.id === taskId);
    
    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    res.json({
      success: true,
      data: task
    });
    
  } catch (error) {
    next(error);
  }
});

// POST /api/tasks - создание новой задачи
router.post('/', validateCreateTask, async (req, res, next) => {
  try {
    const { title, description, category, priority, dueDate } = req.body;
    const data = await readData();
    
    const newTask = {
      id: await getNextId(),
      uuid: uuidv4(),
      title,
      description: description || '',
      category: category || 'personal',
      priority: priority || 3,
      dueDate: dueDate || null,
      completed: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    // Перечитываем данные после getNextId так как он мог изменить файл
    const freshData = await readData();
    freshData.tasks.push(newTask);
    await writeData(freshData);
    
    res.status(201).json({
      success: true,
      message: 'Задача успешно создана',
      data: newTask
    });
    
  } catch (error) {
    next(error);
  }
});

// PUT /api/tasks/:id - полное обновление задачи
router.put('/:id', validateId, validateUpdateTask, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const updates = req.body;
    const data = await readData();
    
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    const updatedTask = {
      ...data.tasks[taskIndex],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    
    data.tasks[taskIndex] = updatedTask;
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача успешно обновлена',
      data: updatedTask
    });
    
  } catch (error) {
    next(error);
  }
});

// PATCH /api/tasks/:id/complete - отметка задачи как выполненной
router.patch('/:id/complete', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    data.tasks[taskIndex].completed = true;
    data.tasks[taskIndex].updatedAt = new Date().toISOString();
    
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача отмечена как выполненная',
      data: data.tasks[taskIndex]
    });
    
  } catch (error) {
    next(error);
  }
});

// DELETE /api/tasks/:id - удаление задачи
router.delete('/:id', validateId, async (req, res, next) => {
  try {
    const taskId = req.params.id;
    const data = await readData();
    
    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    
    if (taskIndex === -1) {
      return res.status(404).json({
        success: false,
        error: 'Задача не найдена'
      });
    }
    
    data.tasks.splice(taskIndex, 1);
    await writeData(data);
    
    res.json({
      success: true,
      message: 'Задача успешно удалена'
    });
    
  } catch (error) {
    next(error);
  }
});

module.exports = router;
