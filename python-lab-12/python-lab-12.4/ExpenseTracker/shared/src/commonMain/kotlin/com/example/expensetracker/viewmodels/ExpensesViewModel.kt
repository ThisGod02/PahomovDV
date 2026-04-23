package com.example.expensetracker.viewmodels

import com.example.expensetracker.db.Database
import com.example.expensetracker.models.Budget
import com.example.expensetracker.models.Category
import com.example.expensetracker.models.CategoryStats
import com.example.expensetracker.models.Expense
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.datetime.Clock
import kotlinx.datetime.LocalDate
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime

class ExpensesViewModel(private val database: Database) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    private val _state = MutableStateFlow(ExpensesState())
    val state: StateFlow<ExpensesState> = _state.asStateFlow()

    private val now = Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault()).date
    private val _currentMonth = MutableStateFlow(LocalDate(now.year, now.monthNumber, 1))

    init { loadData() }

    private fun loadData() {
        combine(
            database.getAllCategories(),
            _currentMonth.flatMapLatest { d -> database.getExpensesForMonth(d.year, d.monthNumber) },
            _currentMonth.flatMapLatest { d -> database.getBudgetForMonth(d.year, d.monthNumber) }
        ) { cats, exps, budgets ->
            _state.update { it.copy(categories = cats, expenses = exps, budgets = budgets, isLoading = false) }
        }.catch { e ->
            _state.update { it.copy(error = e.message, isLoading = false) }
        }.launchIn(scope)
    }

    fun addExpense(amount: Double, categoryId: Long, description: String?) {
        scope.launch {
            database.insertExpense(Expense(0, amount, categoryId, description, Clock.System.now()))
        }
    }

    fun deleteExpense(id: Long) { scope.launch { database.deleteExpense(id) } }

    fun previousMonth() {
        val c = _currentMonth.value
        _currentMonth.value = if (c.monthNumber == 1) LocalDate(c.year - 1, 12, 1)
                              else LocalDate(c.year, c.monthNumber - 1, 1)
    }

    fun nextMonth() {
        val c = _currentMonth.value
        _currentMonth.value = if (c.monthNumber == 12) LocalDate(c.year + 1, 1, 1)
                              else LocalDate(c.year, c.monthNumber + 1, 1)
    }

    // Установка/обновление бюджета
    fun setBudget(categoryId: Long, amount: Double) {
        scope.launch {
            val existing = _state.value.budgets.find { it.categoryId == categoryId }
            if (existing != null) {
                database.updateBudget(existing.copy(amount = amount))
            } else {
                val monthStart = _currentMonth.value
                    .atStartOfDayIn(TimeZone.currentSystemDefault())
                database.insertBudget(Budget(0, categoryId, amount, monthStart))
            }
        }
    }

    fun clearError() { _state.update { it.copy(error = null) } }
    fun onCleared() { scope.cancel() }
}

data class ExpensesState(
    val categories: List<Category> = emptyList(),
    val expenses: List<Expense> = emptyList(),
    val budgets: List<Budget> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
) {
    val totalExpenses: Double get() = expenses.sumOf { it.amount }

    val expensesByCategory: Map<Long, Double>
        get() = expenses.groupBy { it.categoryId }.mapValues { (_, list) -> list.sumOf { it.amount } }

    // Топ-3 категории по расходам
    val topCategories: List<Pair<Category, Double>>
        get() = categories.mapNotNull { cat ->
            expensesByCategory[cat.id]?.let { cat to it }
        }.sortedByDescending { it.second }.take(3)

    // Статистика по всем категориям
    fun getCategoryStats(budgets: List<Budget>): List<CategoryStats> =
        categories.map { cat ->
            val spent = expensesByCategory[cat.id] ?: 0.0
            val budget = budgets.find { it.categoryId == cat.id }
            CategoryStats(cat, spent, budget?.amount, expenses.count { it.categoryId == cat.id })
        }
}
